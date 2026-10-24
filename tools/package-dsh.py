"""Build and read back the standalone DSH distribution without installing it."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,tarfile,io,gzip
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=R/'dist');a=p.parse_args()
 pkg=json.loads((R/'package.json').read_text(encoding='utf-8'))
 assert pkg['name']=='dsh-furry-partner' and 'pi' not in pkg
 rows=json.loads(subprocess.check_output(['npm.cmd' if os.name=='nt' else 'npm','pack','--dry-run','--json','--ignore-scripts'],cwd=R,text=True,encoding='utf-8'))[0]['files']
 a.out.mkdir(parents=True,exist_ok=True);out=a.out/f'dsh-furry-partner-{pkg["version"]}.tgz';assert not out.exists(),'Preserve earlier packages'
 files=[]
 with out.open('wb') as stream,gzip.GzipFile(fileobj=stream,mode='wb',mtime=0) as zipped,tarfile.open(fileobj=zipped,mode='w') as tar:
  for row in rows:
   name=row['path'];path=(R/name).resolve();assert path.is_relative_to(R) and path.is_file() and not path.is_symlink()
   if name.startswith('assets/animated/provenance/') and path.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.mp4'}:continue
   assert name not in {'index.ts','install.ps1','uninstall.ps1'}
   data=path.read_bytes();info=tarfile.TarInfo('package/'+name);info.size=len(data);info.mode=0o644;tar.addfile(info,io.BytesIO(data))
   files.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 expected={r['path']:r for r in files}
 with tarfile.open(out) as tar:
  seen=set()
  for m in tar:
   name=m.name.removeprefix('package/');assert name in expected and name not in seen and m.isfile()
   assert hashlib.sha256(tar.extractfile(m).read()).hexdigest()==expected[name]['sha256'];seen.add(name)
  assert seen==set(expected)
 digest=hashlib.file_digest(out.open('rb'),'sha256').hexdigest()
 report={'package':pkg['name'],'version':pkg['version'],'archive':str(out),'archiveBytes':out.stat().st_size,'sha256':digest,'allArchiveEntriesVerified':True,'fileCount':len(files),'files':files}
 out.with_suffix('.tgz.sha256').write_text(f'{digest}  {out.name}\n',encoding='utf-8')
 out.with_suffix('.report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k!='files'}))
if __name__=='__main__':main()
