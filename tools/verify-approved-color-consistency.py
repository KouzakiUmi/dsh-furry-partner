"""Verify shipped HD frames against the approved color derivation.

The approval chain signs a reconstruction: the frozen source29 baseline pushed
through the frozen transforms. That reconstruction is rebuilt here and every
shipped frame is held to it -- alpha must be byte-identical to the approved
pixels, and alpha-weighted RGB error must stay inside the lossy re-encode
tolerance. Indexed payloads, palette and clock keep their exact approved
assertions.

The transform is the expensive step, so it runs on the GPU when a ROCm/CUDA
torch build is importable and falls back to the frozen numpy module otherwise.
`--check-gpu` proves the two agree bit-for-bit before the GPU path is trusted.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import argparse,copy,hashlib,importlib.util,json,os
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parent.parent;A=R/'assets/animated';S=R/'Hi-Res'
P=A/'provenance/color-consistency-20261024'

# Alpha is never tolerated: it drives compositing, so it must equal the approved
# pixels. RGB is alpha-weighted because a pixel at alpha 8 contributes 3% of the
# blend -- unweighted error there says nothing about what a user can see.
ALPHA_WEIGHTED_PSNR_MIN=35.0
ALPHA_WEIGHTED_DELTA_E_MAX=2.2
WORKERS=4

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bh(v):return hashlib.sha256(v).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(Path(p).read_text(encoding='utf8'))
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


# --- Optional GPU port of frozen-v1.transform ---------------------------------
# frozen-v1 computes smooth(a[:,:,3],16,160) on the raw uint8 alpha array, so
# (alpha-16) wraps below 16 and visible becomes 1.0 there. That quirk is part of
# the approved chain, so the port reproduces it instead of correcting it.
_GPU = {'torch': None, 'luma': None, 'target': None, 'target_luma': None}

def _gpu_ready():
    if _GPU['torch'] is not None:
        return _GPU['torch'] is not False
    try:
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError('no accelerator')
        dev = 'cuda'
        _GPU['torch'] = torch
        _GPU['luma'] = torch.tensor([.2126, .7152, .0722], dtype=torch.float64, device=dev)
        _GPU['target'] = torch.tensor([80., 97., 117.], dtype=torch.float64, device=dev)
        _GPU['target_luma'] = float((_GPU['target'] @ _GPU['luma']).item())
        return True
    except Exception:
        _GPU['torch'] = False
        return False

def _gs(x, a, b, torch):
    t = torch.clamp((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

def _gpu_smooth_uint8(alpha_u8, a, b, torch):
    wrapped = (alpha_u8 - torch.tensor(a, dtype=torch.uint8, device='cuda')) % 256
    return _gs(wrapped.to(torch.float64), 0, b - a, torch)

def transform_approved(a, clip, rect):
    """Return the approved pixels for one frame, on GPU when available."""
    if not _gpu_ready():
        v1, a02 = _transforms()
        out, _ = v1.transform(a, clip, rect)
        return out
    torch = _GPU['torch']; LUMA = _GPU['luma']; TARGET = _GPU['target']; TL = _GPU['target_luma']
    t = torch.from_numpy(np.ascontiguousarray(a)).to('cuda')
    rgb = t[:, :, :3].to(torch.float64)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = rgb @ LUMA
    spread = rgb.max(2).values - rgb.min(2).values
    visible = _gpu_smooth_uint8(t[:, :, 3], 16, 160, torch)
    H, W = a.shape[0], a.shape[1]
    py = torch.arange(H, device='cuda', dtype=torch.float64)[:, None]
    px = torch.arange(W, device='cuda', dtype=torch.float64)[None, :]
    xx = px * rect['width'] / W + rect['x']
    yy = py * rect['height'] / H + rect['y']
    neutral = (_gs(torch.maximum(r - b, g - b), .7, 4, torch) * (1 - _gs(spread, 18, 34, torch))
               * _gs(y, 35, 80, torch) * visible)
    if clip == 'search':
        paper = (yy >= 450) & ((xx < 405) | (yy >= 590)) & (rgb.min(2).values > 155)
        neutral = neutral.masked_fill(paper, 0)
    excess = (g - r) - (TARGET[1].item() - TARGET[0].item()) / (TARGET[2].item() - TARGET[0].item()) * (b - r)
    cloth = (_gs(torch.abs(excess), 1, 6, torch) * _gs(b - r, 7, 18, torch) * (1 - _gs(spread, 65, 90, torch))
             * _gs(y, 24, 45, torch) * (1 - _gs(rgb.max(2).values, 165, 185, torch)) * visible)
    if clip in ['work', 'work-enter', 'work-exit']:
        cloth = cloth.masked_fill((yy >= 500) & (xx >= 90) & (xx <= 560), 0)
    if clip == 'watch':
        face = ((xx - 320) / 170) ** 2 + ((yy - 300) / 133) ** 2 <= 1
        handle = (xx >= 170) & (xx <= 320) & (yy >= 345) & (yy <= 515) & (b > r + 18) & (b > g + 10)
        cloth = cloth.masked_fill(face | handle, 0)
    neutral_rgb = y[:, :, None].expand_as(rgb)
    desired = y[:, :, None] + ((b - r) / (TARGET[2].item() - TARGET[0].item()))[:, :, None] * (TARGET - TL)
    result = rgb + (neutral_rgb - rgb) * neutral[:, :, None] + (desired - rgb) * cloth[:, :, None]
    out = t.clone()
    out[:, :, :3] = torch.clamp(torch.round(result), 0, 255).to(torch.uint8)
    zero = (t[:, :, 3] == 0).unsqueeze(-1).expand_as(out[:, :, :3])
    out[:, :, :3] = torch.where(zero, t[:, :, :3], out[:, :, :3])
    return out.cpu().numpy()

def freeze_approved(a, clip, rect):
    """Apply the affection-only a02 pass when the clip needs it."""
    out = transform_approved(a, clip, rect)
    if clip == 'affection':
        _, a02 = _transforms()
        out = a02.transform_v1_affection(out)
    return out

def lab(rgb):
 a=rgb.astype(np.float64)/255.0
 lin=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
 M=np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]])
 xyz=lin@M.T;white=np.array([0.95047,1.0,1.08883]);t=xyz/white
 f=np.where(t>0.008856,np.cbrt(t),7.787*t+16/116)
 return 116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])

def noncolor(raw):
 raw=copy.deepcopy(raw);raw.pop('palette');raw.pop('revision')
 for f in raw['frames']:f.pop('pixels')
 return raw

# Worker-side module handles, populated once per process.
_V1=None;_A02=None

def _transforms():
 global _V1,_A02
 if _V1 is None:
  _V1=mod(P/'frozen-v1.py','verify_color_frozen_v1')
  _A02=mod(P/'frozen-a02.py','verify_color_frozen_a02')
 return _V1,_A02

def check_frame(task):
 """Rebuild the approved pixels for one frame and hold the shipped frame to them."""
 global ST
 try:
  ST
 except NameError:
  ST=mod(R/'tools/stage-motion-polish.py','verify_color_stage')
 cid,rect,f,rr=task
 current=A/'hires'/cid/f['file'];original=S/'hires'/cid/f['file']
 assert sha(current)==f['webpSha256']
 assert sha(original)==rr['originalWebpSha256']

 base=np.array(Image.open(original).convert('RGBA'))
 assert bh(base.tobytes())==rr['originalDecodedRgbaSha256']
 assert bh(base[:,:,3].tobytes())==rr['alphaSha256']
 assert bh(base[base[:,:,3]==0,:3].tobytes())==rr['alpha0RgbSha256']

 approved=freeze_approved(base,cid,rect)
 assert bh(approved.tobytes())==rr['approvedDecodedRgbaSha256'],(cid,f['file'],'approved reconstruction')

 b=np.array(Image.open(current).convert('RGBA'))
 assert approved.shape==b.shape==(rect['height'],rect['width'],4)
 assert bh(b.tobytes())==f['decodedRgbaSha256']
 assert np.array_equal(approved[:,:,3],b[:,:,3]),(cid,f['file'],'alpha changed by re-encode')

 alpha=approved[:,:,3].astype(np.float64)/255.0;vis=alpha>0
 if vis.any():
  d=(approved[:,:,:3].astype(np.float64)-b[:,:,:3].astype(np.float64))**2
  wmse=float((d.sum(axis=2)*alpha).sum()/(alpha.sum()*3))
  psnr=99.0 if wmse==0 else 10*np.log10(255.0**2/wmse)
  assert psnr>=ALPHA_WEIGHTED_PSNR_MIN,(cid,f['file'],'alpha-weighted PSNR',round(psnr,2))
  La,aa,ba=lab(approved[:,:,:3][vis]);Lb,ab,bb=lab(b[:,:,:3][vis])
  dE=np.sqrt((La-Lb)**2+(aa-ab)**2+(ba-bb)**2)
  dEmean=float((dE*alpha[vis]).sum()/alpha[vis].sum())
  assert dEmean<=ALPHA_WEIGHTED_DELTA_E_MAX,(cid,f['file'],'alpha-weighted deltaE',round(dEmean,2))

 assert f['sourceAsset']=={'path':current.relative_to(R).as_posix(),'webpSha256':sha(current),'decodedRgbaSha256':bh(b.tobytes())}
 return True


def selfcheck_gpu(sample_per_clip=2):
    """Prove the GPU port reproduces frozen-v1 bit-for-bit before trusting it."""
    _GPU['torch'] = None
    if not _gpu_ready():
        print('gpu self-check: no accelerator, CPU path only', flush=True)
        return None
    obj = json.loads((A/'catalog.json').read_text(encoding='utf-8'))
    v1 = mod(P/'frozen-v1.py', 'verify_color_frozen_v1')
    a02 = mod(P/'frozen-a02.py', 'verify_color_frozen_a02')
    checked = 0
    for cid, clip in obj['clips'].items():
        if clip.get('qa', {}).get('accepted') is not True:
            continue
        rect = clip['paintRect']
        for f in clip['hires']['frames'][:sample_per_clip]:
            base = np.array(Image.open(S/'hires'/cid/f['file']).convert('RGBA'))
            ref, _ = v1.transform(base, cid, rect)
            if cid == 'affection':
                ref = a02.transform_v1_affection(ref)
            got = freeze_approved(base, cid, rect)
            assert np.array_equal(ref, got), f'{cid}/{f["file"]}: GPU differs from frozen-v1'
            checked += 1
    print(f'gpu self-check: {checked} frames bit-identical to frozen-v1', flush=True)
    return checked

def run(reproduce=False):
 global ST,WORKERS
 ST=mod(R/'tools/stage-motion-polish.py','verify_color_stage')
 c=read(A/'catalog.json');ref=c['colorDerivativeProvenance'];p=A/ref['file']
 assert sha(p)==ref['sha256'];proof=read(p)
 assert sha(S/'catalog.json')==proof['sourceCatalog']['sha256']=='f8de911e18da73a6d091a9193c667dfcf6350374c0509b5c1c69c82b133150c1';old=read(S/'catalog.json')
 approval=P/'user-final-approval.json';assert sha(approval)==ref['approvalSha256']=='521fbc24a412ead022e9d86a49f3acaf1b2769c566342580fb1adb076cc604fc';ap=read(approval);assert ap['allowCanonicalColorReplacement'] is True and ap['clipCount']==29
 for i in proof['inputs'].values():assert sha(R/i['file'])==i['sha256']
 assert c['revision']==proof['revision'] and c['revision']!=old['revision'];assert len(c['clips'])==29
 for k,v in old.items():
  if k not in ['clips','revision','indexedBinaryProvenance']:assert c[k]==v,('topMetadata',k)
 palette=read(P/'common-palette.json')['palette'];assert bh(canonical(palette))==proof['commonPaletteSha256'];indexed=0;tasks=[]
 for cid,clip in c['clips'].items():
  prev=old['clips'][cid];rec=proof['clips'][cid];assert ap['clipChoices'][cid]==rec['variant'];assert clip['qa']==prev['qa'];assert clip['paintRect']==prev['paintRect']
  for k,v in prev.items():
   if k not in ['indexed','hires']:assert clip[k]==v,(cid,k)
  for k,v in prev['hires'].items():
   if k!='frames':assert clip['hires'][k]==v
  assert len(clip['hires']['frames'])==len(prev['hires']['frames'])==len(rec['frames'])
  for f,of,rr in zip(clip['hires']['frames'],prev['hires']['frames'],rec['frames']):
   for k,v in of.items():
    if k not in ['sourceAsset','webpSha256','decodedRgbaSha256']:assert f[k]==v,(cid,f['file'],k)
   tasks.append((cid,clip['paintRect'],f,rr))
  raw=ST.decode_indexed(A/clip['indexed']['umi']['file']);original=ST.decode_indexed(S/prev['indexed']['umi']['file']);assert noncolor(raw)==noncolor(original);assert bh(canonical(noncolor(raw)))==rec['indexed']['priorNoncolorMetadataSha256'];assert raw['revision']==c['revision'];assert raw['palette']==palette
  restored=copy.deepcopy(raw);restored['revision']=old['revision'];assert bh(canonical(restored))==rec['indexed']['approvedCandidateCanonicalDecodedSha256'],cid
  assert sha(A/clip['indexed']['umi']['file'])==rec['indexed']['sha256'];assert bh(canonical(raw))==rec['indexed']['sourceJsonSha256']
  for style,entry in clip['indexed'].items():
   assert entry['sha256']==rec['indexed']['sha256'] and entry['sourceJsonSha256']==rec['indexed']['sourceJsonSha256'];oe=prev['indexed'][style]
   for k,v in oe.items():
    if k not in ['sha256','sourceJsonSha256']:assert entry[k]==v
  indexed+=len(raw['frames'])
 with ProcessPoolExecutor(max_workers=WORKERS) as pool:
  for ok in pool.map(check_frame,tasks,chunksize=16):assert ok
 assert len(tasks)==proof['hdFrameCount']==3048 and indexed==proof['piFrameCount']
 result={'passed':True,'clipCount':29,'HDWholeRGBAFrames':len(tasks),'HDAlphaExact':True,'HDRgbWithinQ90Tolerance':True,'alphaWeightedPsnrMin':ALPHA_WEIGHTED_PSNR_MIN,'alphaWeightedDeltaEMax':ALPHA_WEIGHTED_DELTA_E_MAX,'PiExactReviewedCandidateFrames':indexed,'PiOriginalNoncolorMetadataExact':True,'sameReviewedCommonPalette':True,'allOriginalQAMetadataRetained':True,'workInputsRequired':False,'approvedReconstructionVerified':True,'catalogRevision':c['revision'],'catalogSha256':sha(A/'catalog.json')}
 print(json.dumps(result),flush=True);return result

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--reproduce',action='store_true')
 ap.add_argument('--workers',type=int,default=4)
 ap.add_argument('--check-gpu',action='store_true')
 args=ap.parse_args();WORKERS=args.workers
 if args.check_gpu:selfcheck_gpu()
 else:run(args.reproduce)
