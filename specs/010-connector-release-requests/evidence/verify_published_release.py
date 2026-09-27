"""Reproduce this release download/hash verification from a repository checkout."""
import hashlib,json,pathlib,urllib.request,zipfile
from datetime import datetime, timezone
from pypdf import PdfReader
repo='AXIOVEX/michigan-workforce-intelligence'
version='2026.09.27.131143Z'
expected_commit='d0fbc71af5dc4a1f2650984105c21517f59f683c'
root=pathlib.Path(__file__).resolve().parents[3]
out=root/'output/pdf'/version
out.mkdir(parents=True,exist_ok=True)
with urllib.request.urlopen(f'https://api.github.com/repos/{repo}/releases/tags/reports-{version}', timeout=60) as response:
 release=json.load(response)
expected={'executive-brief.pdf','jobs-economic-report.pdf','job-continuity-solutions.pdf','manifest.json','SHA256SUMS.txt',f'reports-{version}.zip'}
assert {a['name'] for a in release['assets']}==expected
for a in release['assets']:
 with urllib.request.urlopen(a['browser_download_url'], timeout=60) as r: data=r.read()
 assert len(data)==a['size']
 (out/a['name']).write_bytes(data)
checks={}
for line in (out/'SHA256SUMS.txt').read_text().splitlines():
 digest,name=line.split('  ',1)
 assert pathlib.Path(name).name==name
 with zipfile.ZipFile(out/f'reports-{version}.zip') as bundle:
  data=(out/name).read_bytes() if (out/name).exists() else bundle.read(name)
 assert hashlib.sha256(data).hexdigest()==digest,name
 checks[name]=digest
assert expected-{'SHA256SUMS.txt'}<=checks.keys()
manifest=json.loads((out/'manifest.json').read_text())
assert manifest['version']==version and manifest['source_commit']==expected_commit
pages={name:len(PdfReader(out/name).pages) for name in expected if name.endswith('.pdf')}
assert pages==manifest['pdf_pages']
with zipfile.ZipFile(out/f'reports-{version}.zip') as archive:
 assert archive.testzip() is None
 for name,digest in manifest['sha256'].items():
  assert hashlib.sha256(archive.read(name)).hexdigest()==digest,name
result={'verified_at':datetime.now(timezone.utc).isoformat(),'release_url':release['html_url'],'release_id':release['id'],'version':version,'source_commit':expected_commit,'assets':[{k:a[k] for k in ['name','size','browser_download_url']} for a in release['assets']],'downloaded_sha256':{name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in sorted(expected)},'pdf_pages':pages,'zip_members_verified':len(manifest['sha256']),'checksums_match':True,'manifest_identity_matches':True}
evidence=root/'specs/010-connector-release-requests/evidence'
(evidence/'published-release-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
