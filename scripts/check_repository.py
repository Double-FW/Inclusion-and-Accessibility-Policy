"""Read-only local source/contract checks; optional public access checks, never publication."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from rebuild_resource_pack import compiled_body

ROOT=Path(__file__).resolve().parents[1]

def check(root=ROOT):
    root=Path(root);errors=[];cfg=json.loads((root/'huggingface/export-config.json').read_text())
    registry=json.loads((root/'sources/public-references.json').read_text());refs=registry['references']
    if len({x['id'] for x in refs})!=len(refs):errors.append('Duplicate public reference IDs')
    allowed={x['repository'] for x in refs}|{cfg['source_repository']}
    for x in refs:
        expected='https://github.com/'+x['repository']+'/blob/'+x['source_commit']+'/'+urllib.parse.quote(x['path'])
        if x.get('public') is not True or x.get('authority')!='secondary_practitioner_guidance' or x['url']!=expected:errors.append('Bad public reference: '+x['id'])
    files=[p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts]
    for p in files:
        if p.suffix not in {'.md','.json','.yaml','.yml'}:continue
        text=p.read_text();name=str(p.relative_to(root))
        for repo in re.findall(r'https://github\.com/(Double-FW/[^\s/<>\)\]\"\x27]+)',text):
            if repo not in allowed:errors.append('Unregistered/non-public dependency: '+name+' -> '+repo)
        if any(x in text for x in ['chatgpt.com/library','account_id=','file_id=libfile_']):errors.append('Private access metadata: '+name)
        if p.suffix!='.md':continue
        if text.count('```')%2:errors.append('Unbalanced fence: '+name)
        # Compiled reader links now resolve to exact copies and are checked too.
        for raw in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
            u=urllib.parse.urlsplit(raw.strip('<>'))
            if u.scheme or u.netloc:continue
            dest=(p.parent/urllib.parse.unquote(u.path)).resolve() if u.path else p
            if not dest.is_relative_to(root.resolve()) or not dest.is_file():errors.append('Local link: '+name+' -> '+raw)
            elif u.fragment:
                anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#{1,6} +(.+)',dest.read_text(),re.M)}
                if urllib.parse.unquote(u.fragment) not in anchors:errors.append('Local anchor: '+name+' -> '+raw)
    prompt=(root/'Policy-Generation-Prompt.md').read_text()
    if prompt.count('## Instructions for the AI assistant — agent-only')!=1:errors.append('Prompt needs one agent-only section')
    for key in ['Draft policy','Clause-to-source and delivery register','Decision and gap log','Approval and review checklist']:
        if key not in prompt:errors.append('Missing output contract: '+key)
    for marker in ['rules.metadata','audit_event','0.0-1.0']:
        if marker in prompt:errors.append('Obsolete technical contract in prompt')
    if 'license: "MIT"' not in (root/'AGENTS.md').read_text():errors.append('AGENTS must declare MIT')
    if any(v!='MIT' for v in cfg['source_licenses'].values()):errors.append('Source licence allocation must be MIT')
    raci=(root/'Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md').read_text()
    for prefix,n in [('H',16),('A',10),('D',6)]:
        ids=re.findall(r'^\| ('+prefix+r'\d{2})\b',raci,re.M)
        if sorted(ids)!=[prefix+f'{i:02d}' for i in range(1,n+1)]:errors.append('RACI identifier inventory: '+prefix)
    for line in raci.splitlines():
        if re.match(r'^\| [HA]\d{2}\b',line):
            a=line.split('|')[3].strip()
            if a not in {'ES','PO','LR','EV','BO','AG','PL'}:errors.append('Exactly one human accountable owner required: '+line[:80])
    pack=root/'Inclusion-Policy-RAG-and-Prompts';manifest=json.loads((pack/'source-manifest.json').read_text())
    if {x['path'] for x in manifest['files']}!=set(cfg['files']+cfg['supporting_files']+['LICENSE']):errors.append('Pack inventory differs from approved sources')
    rag=(pack/'RAG_Reference.md').read_text()
    for row in manifest['files']:
        data=(root/row['path']).read_bytes();copied=(pack/'Sources'/row['path']).read_bytes()
        if data!=copied or hashlib.sha256(data).hexdigest()!=row['sha256'] or len(data)!=row['bytes']:errors.append('Stale source copy/hash: '+row['path'])
        if hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()!=row['git_blob_sha']:errors.append('Stale source blob: '+row['path'])
        if compiled_body(row['path'],data.decode()) not in rag:errors.append('Compiled source incomplete: '+row['path'])
    return {'status':'passed' if not errors else 'failed','errors':errors,'public_working_references':len(refs),
      'required_policy_outputs':4,'review_scenarios':8,'scope':'Structural/source preservation and cross-document contracts; no LLM, product, participant or legal assessment.'}

def live_links(root=ROOT):
    refs=json.loads((Path(root)/'sources/public-references.json').read_text())['references']
    def verify(x):
        req=urllib.request.Request('https://api.github.com/repos/'+x['repository'],headers={'User-Agent':'Double-FW-policy-reference-check'})
        with urllib.request.urlopen(req,timeout=30) as response:meta=json.load(response)
        if meta.get('private') is not False or meta.get('full_name')!=x['repository']:raise ValueError(x['id']+' is not confirmed public')
        url='https://raw.githubusercontent.com/'+x['repository']+'/'+x['source_commit']+'/'+urllib.parse.quote(x['path'])
        with urllib.request.urlopen(url,timeout=30) as response:data=response.read()
        if hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()!=x['source_blob_sha']:raise ValueError(x['id']+' source bytes differ')
        return x['id']
    with ThreadPoolExecutor(max_workers=4) as pool:ids=list(pool.map(verify,refs))
    return {'public_files_verified':len(ids),'scope':'Unauthenticated public access and pinned source-byte identity, not legal currency or onward-source completeness.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--live-links',action='store_true');args=parser.parse_args()
    report=check()
    if report['errors']:print(json.dumps(report,indent=2));raise SystemExit(1)
    if args.live_links:
        try:report['live_links']=live_links()
        except Exception as exc:report['status']='failed';report['errors'].append(type(exc).__name__+': public reference verification did not complete')
    print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
