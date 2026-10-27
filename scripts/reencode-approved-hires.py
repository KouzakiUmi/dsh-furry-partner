"""Re-encode approved 896px HD frames from lossless to lossy WebP (q90).

Alpha bytes are preserved exactly; only RGB changes. Writes into
assets/animated/hires in place and records a per-frame report so the catalog
hashes and approval chain can be rebuilt from measured facts.

Usage:
  python scripts/reencode-approved-hires.py --check      # dry-run, no writes
  python scripts/reencode-approved-hires.py --apply      # rewrite frames
"""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import argparse, hashlib, io, json, os

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
HIRES = ROOT / 'assets' / 'animated' / 'hires'
QUALITY = 90
METHOD = 6


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def encode_one(path_str):
    path = Path(path_str)
    before = path.read_bytes()
    im = Image.open(io.BytesIO(before)).convert('RGBA')
    a = np.asarray(im)
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=QUALITY, method=METHOD)
    out = buf.getvalue()
    after = np.asarray(Image.open(io.BytesIO(out)).convert('RGBA'))
    if not np.array_equal(a[:, :, 3], after[:, :, 3]):
        raise RuntimeError(f'alpha changed: {path}')
    opaque = a[:, :, 3] == 255
    if opaque.any():
        d = (a[:, :, :3][opaque].astype(np.int16) - after[:, :, :3][opaque].astype(np.int16))
        mse = float((d.astype(np.float64) ** 2).mean())
        psnr = 10 * np.log10(255.0 ** 2 / mse) if mse > 0 else 99.0
    else:
        psnr = 99.0
    return {
        'path': path.relative_to(ROOT).as_posix(),
        'beforeBytes': len(before),
        'afterBytes': len(out),
        'beforeWebpSha256': sha_bytes(before),
        'afterWebpSha256': sha_bytes(out),
        'beforeDecodedRgbaSha256': sha_bytes(a.tobytes()),
        'afterDecodedRgbaSha256': sha_bytes(after.tobytes()),
        'alphaEqual': True,
        'opaquePsnr': round(psnr, 2),
        '_bytes': out,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--workers', type=int, default=max(2, (os.cpu_count() or 4) - 1))
    args = ap.parse_args()
    if not (args.apply or args.check):
        ap.error('choose --check or --apply')

    files = sorted(p.as_posix() for p in HIRES.rglob('*.webp'))
    print(f'frames: {len(files)}  workers: {args.workers}', flush=True)

    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i, r in enumerate(pool.map(encode_one, files, chunksize=8), 1):
            results.append(r)
            if i % 250 == 0:
                print(f'  {i}/{len(files)}', flush=True)

    total_before = sum(r['beforeBytes'] for r in results)
    total_after = sum(r['afterBytes'] for r in results)
    psnrs = [r['opaquePsnr'] for r in results]
    print(f"bytes {total_before/1048576:.1f} MB -> {total_after/1048576:.1f} MB "
          f"({total_before/total_after:.2f}x)")
    print(f"opaque PSNR mean {np.mean(psnrs):.2f} min {min(psnrs):.2f}")

    if args.check:
        print('dry run, nothing written')
        return

    for r in results:
        Path(ROOT / r['path']).write_bytes(r['_bytes'])
    report = [{k: v for k, v in r.items() if k != '_bytes'} for r in results]
    out = ROOT / 'assets' / 'animated' / 'provenance' / 'lossy-q90-reencode.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'quality': QUALITY, 'method': METHOD, 'frameCount': len(report),
        'totalBeforeBytes': total_before, 'totalAfterBytes': total_after,
        'alphaPreservedExactly': True,
        'frames': report,
    }, indent=2) + '\n', encoding='utf-8')
    print('wrote', out.relative_to(ROOT))


if __name__ == '__main__':
    main()
