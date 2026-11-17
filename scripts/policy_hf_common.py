"""Fixed source/destination and committed-source integrity for the inclusion and accessibility policy dataset."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import urllib.request

SOURCE = 'Double-FW/Inclusion-and-Accessibility-Policy'
TARGET = 'GarethFW/Disability_Inclusion_and_Accessibility_Policy'
ROOT = Path(__file__).resolve().parents[1]
MANAGED = ('README.md', 'LICENSE', 'NOTICE.md', 'documents.jsonl', 'knowledge_chunks.jsonl',
           'provenance.json', 'record_schema.json', 'validation_report.json')
REQUIRED_CONTEXT = {'AGENTS.md', 'README.md', 'Programme_Operating_and_Reporting_Map.md', 'Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md', 'Accessibility_and_Inclusion_Policy_Creation_Guide.md', 'Policy-Generation-Prompt.md'}
EXCLUDED_PREFIXES = ('Inclusion-Policy-RAG-and-Prompts/',)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def destination(value):
    if value != TARGET:
        raise ValueError('Destination must be ' + TARGET + '.')
    return value

def load_config(root=ROOT):
    # Configuration and documents come from the same committed snapshot.
    attrs = git(root, 'ls-tree', 'HEAD', '--', 'huggingface/export-config.json').decode()
    if not attrs.startswith('100644 blob '):
        raise ValueError('Export configuration must be a committed regular file.')
    cfg = json.loads(git(root, 'show', 'HEAD:huggingface/export-config.json'))
    if cfg['source_repository'] != SOURCE:
        raise ValueError('Source must be the approved public inclusion and accessibility policy repository.')
    destination(cfg['destination_dataset'])
    paths = cfg['files']
    if not isinstance(paths, list) or not paths or not all(isinstance(p,str) for p in paths) or len(set(paths)) != len(paths):
        raise ValueError('Approved paths must be a nonempty unique string list.')
    if any(p.startswith(EXCLUDED_PREFIXES) for p in paths):
        raise ValueError('Historical RAG and duplicated source snapshots are excluded from dataset views.')
    for path in paths:
        p = PurePosixPath(path)
        if p.is_absolute() or '..' in p.parts or any(x.startswith('.') for x in p.parts) or p.suffix != '.md':
            raise ValueError('Only approved Markdown source paths may be exported.')
    if set(cfg['required_files']) != set(paths + ['LICENSE']):
        raise ValueError('All approved documents and LICENSE must be required.')
    for field in ('document_only_files','context_files'):
        values = cfg[field]
        if not isinstance(values,list) or not all(isinstance(x,str) for x in values) or len(set(values)) != len(values) or not set(values) <= set(paths):
            raise ValueError(field + ' must contain unique approved paths.')
    if not REQUIRED_CONTEXT <= set(cfg['context_files']):
        raise ValueError('Policy governance, creation/RACI guides, prompt, programme map and orientation must be retained.')
    expected={p:'CC-BY-4.0' if p=='AGENTS.md' else 'MIT' for p in paths}
    if cfg.get('source_licenses') != expected:
        raise ValueError('Preserve root MIT and the file-specific CC BY 4.0 notice; review any changed licence allocation.')
    return cfg

def public_source():
    request = urllib.request.Request('https://api.github.com/repos/' + SOURCE,
        headers={'User-Agent':'Double-FW-inclusion-policy-dataset-export'})
    with urllib.request.urlopen(request,timeout=30) as response:
        info=json.load(response)
    if info.get('full_name') != SOURCE or info.get('private') is not False or info.get('visibility') != 'public':
        raise ValueError('Publishing requires the approved public inclusion and accessibility policy source repository.')

def read_sources(root,cfg):
    tree={}
    for item in git(root,'ls-tree','-rz','--full-tree','HEAD').split(b'\0'):
        if not item:continue
        attrs,raw_path=item.split(b'\t',1)
        mode,kind,sha=attrs.decode().split();tree[raw_path.decode()] = (mode,kind,sha)
    sources,manifest={},[]
    for path in cfg['files']+['LICENSE']:
        if path not in tree:raise ValueError('Required source is missing: '+path)
        mode,kind,sha=tree[path]
        if mode!='100644' or kind!='blob':raise ValueError('Source must be a committed regular file: '+path)
        data=git(root,'cat-file','blob',sha)
        if hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()!=sha:raise ValueError('Git blob integrity failed.')
        sources[path]=data.decode('utf-8')
        if any(marker in sources[path] for marker in ('chatgpt.com/library', 'account_id=', 'file_id=libfile_')):
            raise ValueError('Private source-access metadata must be removed before public export: '+path)
        manifest.append({'path':path,'git_blob_sha':sha,'sha256':digest(data),'size_bytes':len(data)})
    if digest(sources['LICENSE'].encode())!=cfg['approved_license_sha256']:
        raise ValueError('Licence changed. Review its terms, metadata and approved checksum before publishing.')
    return sources,manifest
