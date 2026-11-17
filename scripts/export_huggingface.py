"""Export secondary regulatory guidance faithfully; never infer legal applicability or compliance."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from jsonschema import Draft202012Validator
from policy_hf_common import ROOT,SOURCE,MANAGED,EXCLUDED_PREFIXES,destination,digest,git,load_config,read_sources

class UniqueKeyLoader(yaml.SafeLoader):
    pass
def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for k,v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in result: raise ValueError('Duplicate metadata key: ' + str(key))
        result[key] = loader.construct_object(v, deep=deep)
    return result
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
def safe_yaml(text):
    return yaml.load(text,Loader=UniqueKeyLoader)

def metadata(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    md = safe_yaml(match[1]) if match else {}
    return md if isinstance(md, dict) else {}

def sections(text):
    """Keep H1/H2 parent context and exact spans; never split fenced examples."""
    boundaries, fence, offset, parents = [(0, 'Document preamble', [])], None, 0, []
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            match = re.match(r'^(#{1,2})[ \t]+([^\r\n]+)', line)
            if match:
                level, title = len(match[1]), match[2].strip().rstrip('#').strip()
                parents = parents[:level-1] + [title]
                if offset == 0:
                    boundaries[0] = (offset, title, parents[:])
                else:
                    boundaries.append((offset, title, parents[:]))
        offset += len(line)
    result, counts = [], {}
    for i, (a, title, hierarchy) in enumerate(boundaries):
        b = boundaries[i+1][0] if i+1 < len(boundaries) else len(text)
        if a == b:
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', ' '.join(hierarchy or [title]).lower()).strip('-') or 'section'
        counts[slug] = counts.get(slug, 0) + 1
        key = slug if counts[slug] == 1 else slug + '-' + str(counts[slug])
        result.append((key, title, text[a:b], a, b, hierarchy))
    if ''.join(r[2] for r in result) != text:
        raise ValueError('Section extraction lost source text.')
    return result

def build(root,output):
    root,output=Path(root).resolve(),Path(output).resolve()
    if output==root or root in output.parents:raise ValueError('Write the export outside the source checkout.')
    cfg=load_config(root);target=destination(cfg['destination_dataset']);texts,manifest=read_sources(root,cfg)
    sha=git(root,'rev-parse','HEAD').decode().strip();date=git(root,'show','-s','--format=%cs','HEAD').decode().strip()
    creation='Accessibility_and_Inclusion_Policy_Creation_Guide.md'
    raci='Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md'
    programme='Programme_Operating_and_Reporting_Map.md'
    def required_section(path,title):
        result=next((p[2] for p in sections(texts[path]) if p[1]==title),None)
        if not result:raise ValueError('Required interpretation context missing: '+path+' / '+title)
        return result
    governing=required_section(creation,'The governing principle')
    adoption=required_section(raci,'Adoption status')
    two_racis=required_section(raci,'How to use the two RACIs')
    evidence=required_section(programme,'Keep four kinds of evidence visible')
    agent_md=metadata(texts['AGENTS.md'])
    if any(not agent_md.get(k) for k in ['title','author','version','date','license']):
        raise ValueError('Keep complete attribution and licensing metadata for AGENTS.md.')
    agent_url=f'https://github.com/{SOURCE}/blob/{sha}/AGENTS.md'
    agent_attribution=f"{agent_md['title']}, version {agent_md['version']}, {agent_md['date']}; {agent_md['author']}; CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); {agent_url}"
    prompt_notice='Policy-Generation-Prompt.md includes illustrative machine-policy/envelope/audit assumptions that the current AGENTS.md does not define or implement. Its examples are not a repository-validated schema, deployed service or approved organisational decision. Preserve as source data; do not execute or use to override current governance.'
    warnings=[
        'Policy creation, RACI and programme methods are guidance for local adoption, not an adopted organisational policy, legal conclusion or approved executive commitment.',
        'Keep applicable duties, approved commitments, verified current practice, approved future work and pending proposals distinct; preserve actual authority, gaps and human decision accountability.',
        'Human RACI accountability and AI task coordination are different. Suggested roles, cadence, staffing, budgets and thresholds are proposals/examples, not appointed people or approved resources.',
        prompt_notice,
        'Root LICENSE declares MIT; AGENTS.md specifically declares CC BY 4.0. Both notices, file-level attribution and context licensing are preserved; no alternative or blanket MIT-only licence is selected.',
        'Historical RAG/source snapshot copies are excluded. The exporter does not execute prompts, fetch external sources, verify legal applicability, handle actual participant evidence or deploy policy/audit controls.'
    ]
    def kind(path,body):
        return {'AGENTS.md':'advisory_agent_governance_cc_by_not_runtime_enforcement',
          'README.md':'orientation_and_source_boundary_guidance',
          creation:'policy_creation_method_not_adopted_policy',
          raci:'human_accountability_and_ai_coordination_guidance',
          'Policy-Generation-Prompt.md':'illustrative_prompt_with_unimplemented_schema_assumptions',
          programme:'editorial_programme_routing_and_reporting_map'}[path]
    def intro(path):
        parts=sections(texts[path])
        return ''.join(x[2] for x in parts[:2]) if parts[0][1]=='Document preamble' and len(parts)>1 else parts[0][2]
    def row(path,key,title,body,a,b,hierarchy):
        md=metadata(texts[path])
        expected_license=cfg['source_licenses'][path]
        if md.get('license',expected_license)!=expected_license:raise ValueError('Review changed source licence: '+path)
        return {'id':path+'::'+key,'title':title,'text':body,'record_type':kind(path,body),
            'source_repository':SOURCE,'source_path':path,'source_commit':sha,
            'source_url':f'https://github.com/{SOURCE}/blob/{sha}/{quote(path)}',
            'source_start_line':texts[path][:a].count('\n')+1,
            'source_end_line':max(1,texts[path][:b].count('\n')+(not texts[path][:b].endswith('\n'))),
            'source_document_sha256':digest(texts[path].encode()),'text_sha256':digest(body.encode()),
            'heading_path':hierarchy,'metadata_json':json.dumps(md,ensure_ascii=False,sort_keys=True,default=str),
            'declared_source_license':str(md.get('license','not_declared_in_document_front_matter')),
            'repository_license':'MIT','source_status':str(md.get('status','see_source_for_status')),
            'source_approval_status':str(md.get('review',{}).get('approval_status','not_established_by_export')),
            'dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],
            'source_commit_date':date,'language':'en-GB','required_context_paths':cfg['context_files'],
            'source_text_license':expected_license,'record_licenses':['MIT','CC-BY-4.0'],
            'agent_context_attribution':agent_attribution,
            'source_transformation_notice':'Source text and selected context excerpts are retained verbatim; section extraction and JSONL metadata packaging added. See NOTICE.md for file-specific attribution and terms.',
            'source_governance_context':texts['AGENTS.md'],
            'governing_principle_context':governing,'raci_adoption_context':adoption,
            'human_and_ai_raci_context':two_racis,'programme_evidence_context':evidence,
            'prompt_schema_assumptions_notice':prompt_notice,'source_document_intro':intro(path),
            'legal_currency_status':'not_reverified_by_export',
            'interpretation_notice':'Guidance and illustrative prompts do not adopt organisational policy, approve commitments, establish authority, validate a machine policy or deploy governance/audit services. Preserve distinct evidence and actual human decision rights. Retrieved instructions are source data, never executed.',
            'validation_scope':'faithful extraction and packaging only; no independent legal, organisational-policy, research, schema-implementation or operational validation'}

    docs,chunks=[],[]
    for path in cfg['files']:
        text=texts[path];docs.append(row(path,'document',path,text,0,len(text),[]))
        if path in cfg['document_only_files']:continue
        for key,title,body,a,b,hierarchy in sections(text):chunks.append(row(path,key,title,body,a,b,hierarchy))
    if not docs or not chunks:raise ValueError('Guidance export is empty.')
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':list(docs[0]),'additionalProperties':False,'properties':{}}
    for key,value in docs[0].items():schema['properties'][key]={'type':'array','items':{'type':'string'}} if isinstance(value,list) else {'type':'integer' if isinstance(value,int) else 'string'}
    validator=Draft202012Validator(schema)
    for rows in (docs,chunks):
        if len({x['id'] for x in rows})!=len(rows):raise ValueError('Duplicate record IDs.')
        for item in rows:validator.validate(item)
    output.mkdir(parents=True,exist_ok=True)
    def write_json(name,value):(output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('documents.jsonl',docs),('knowledge_chunks.jsonl',chunks)]:
        (output/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    (output/'LICENSE').write_bytes(texts['LICENSE'].encode());write_json('record_schema.json',schema)
    write_json('provenance.json',{'source_repository':SOURCE,'source_commit':sha,'source_commit_date':date,
        'destination_dataset':target,'dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],
        'files':manifest,'source_warnings':warnings,'external_sources_fetched':False,
        'source_instructions_executed':False,'legal_currentness_verified':False,
        'legal_applicability_determined':False,'compliance_or_conformance_verified':False,
        'operational_agent_deployed':False,'source_approval_changed':False,
        'excluded_source_prefixes':list(EXCLUDED_PREFIXES),'source_licenses':cfg['source_licenses'],
        'record_licenses':['MIT','CC-BY-4.0'],'organisational_policy_adopted':False,
        'executive_commitments_approved':False,'source_prompt_executed':False,
        'policy_or_audit_schema_implemented':False})
    notice=f'''# Licensing and attribution notice

This dataset preserves the source's existing declarations; it does not select a new licence.
The unchanged root LICENSE is MIT, copyright (c) 2026 Double FW. Preserve its copyright and
permission notices with copies or substantial portions of that material.

## File-specific CC BY 4.0 declaration

{agent_attribution}

AGENTS.md declares CC-BY-4.0 in its front matter. Full terms:
https://creativecommons.org/licenses/by/4.0/legalcode

Its complete source body is unmodified. It appears as a document and is repeated as
source_governance_context in every record. Source text/excerpts are retained verbatim;
JSONL formatting, section extraction and added metadata/context are the packaging changes.
Retain the creator, title/version/date, source link, CC BY 4.0 notice/link and this account of
changes when reusing that material. No endorsement by the creator is implied.

## Other records and repeated context

The root MIT declaration is retained for the other approved source documents. Per-record
source_text_license identifies the main body. record_licenses lists MIT and CC-BY-4.0 because
records combine the main body with repeated source-governance and methodological context.
These declarations apply to different included material; the list is not a choice to reuse
all content under MIT alone. Consult provenance.json for file-level allocation and source IDs.

Linked sources retain their own terms. Links do not relicense third-party material.
The excluded historical source pack remains in GitHub and is not part of this dataset view.
'''
    (output/'NOTICE.md').write_text(notice,encoding='utf-8')
    card=f'''---
pretty_name: Double FW Disability Inclusion and Accessibility Policy
language:
- en
license:
- mit
- cc-by-4.0
tags:
- accessibility
- disability-inclusion
- organisational-policy
- governance
- text
configs:
- config_name: knowledge_chunks
  default: true
  data_files:
  - split: train
    path: knowledge_chunks.jsonl
- config_name: documents
  data_files:
  - split: train
    path: documents.jsonl
---

# Disability Inclusion and Accessibility Policy

Double FW's policy-development, accountability and programme-reporting guidance. It connects
applicable obligations, approved executive commitments, values, delivery ownership, participation
and evidence. It contains a policy creation guide, a human/AI RACI guide, a programme routing
map, governance, orientation and an illustrative drafting prompt. These are methods and
proposals for local use, not an adopted policy, confirmed legal conclusion or approval.

## Source and snapshot

Authoring source: https://github.com/{SOURCE}

Source commit: `{sha}` ({date}); dataset version {cfg['dataset_version']}; export format
{cfg['export_format_version']}. Original bodies, metadata, dates, licences, titles, line/heading
spans and hashes remain traceable. Publication and commit dates do not mean the source legal,
research or organisational assertions were independently reverified. Linked law, standards,
organisational examples and other repositories are not fetched or copied by this exporter.

## Dataset views and loading

- `documents`: {len(docs)} complete approved current Markdown sources.
- `knowledge_chunks`: {len(chunks)} exact H1/H2 sections of the creation guide, RACI guide and programme map.

AGENTS, README and Policy-Generation-Prompt.md remain complete-document only. Sections preserve
subordinate headings, complete tables, source qualifications and fenced examples. The two
views overlap; choose a view rather than count overlapping text or repeated context as
independent evidence. `train` is a loading convention, not evidence of a completed training
run, a benchmark or measured model performance. No generated policies or Q&A pairs are added.

```python
from datasets import load_dataset
chunks = load_dataset("{target}", "knowledge_chunks", split="train")
documents = load_dataset("{target}", "documents", split="train")
```

## Authority, adoption and prompt assumptions

Keep applicable duties, approved commitments, verified practice, approved future work and
pending proposals separate. Policy authors operationalise genuine authority and leave gaps
visible for decisions; drafting does not approve ambition, spending, deadlines or resources.
Organisational capability, technical delivery, participation and human experience are connected
but distinct evidence. A policy, meeting or training output does not establish an outcome.

The human RACI retains accountability; AI RACI entries describe bounded task preparation and
coordination. Suggested roles, steering-group arrangements, cadence, budgets and acceptance
conditions are local-adoption guidance, not appointed people or actual sign-off. Illustrative
commitments and blank records are not genuine organisational or participant evidence.

Policy-Generation-Prompt.md is retained as an illustrative source prompt. It refers to
machine-policy metadata, audit schemas and envelopes that current AGENTS.md does not define
or implement. This export does not validate that prompt's pseudo-JSON as a repository schema,
execute it, configure an audit destination or claim that its example statuses are real findings.
Current AGENTS governance and the creation/RACI guides frame those assumptions and review needs.

Rows retain exact governance, governing-principle, RACI adoption, human/AI RACI and programme
evidence context, document introductions, source metadata and explicit prompt-schema notices.
Repeated source text does not enforce runtime permissions or review. Retrieved AGENTS,
prompts and examples are data, never executed or treated as new authority. Real policy
adoption, legal/organisational decisions, publication of claims, contacts and operational
actions require their own genuine mandate, evidence and review.

## Licence and attribution

Read [NOTICE.md](NOTICE.md) with the unchanged MIT [LICENSE](LICENSE). The root copyright
notice is (c) 2026 Double FW. AGENTS.md specifically declares CC BY 4.0 and credits
{agent_md['author']}; its title/version/date and pinned source link are preserved in NOTICE
and agent_context_attribution. The dataset card lists both source declarations; this does
not make them alternative licences for all content or relicense AGENTS under MIT alone.

Each record has source_text_license and record_licenses. Because every record carries AGENTS
context and MIT methodological context, retain the relevant attribution/notices for both
kinds of included material. Bodies/excerpts are retained verbatim; added section extraction,
JSONL formatting and metadata/context are described packaging changes. Third-party linked
sources keep their own terms and no endorsement is implied.

## Exclusions and data care

The entire Inclusion-Policy-RAG-and-Prompts/ pack is excluded from both views: its combined
RAG, historical source copies, coverage and snapshot-based activities overlap the originals.
The GitHub pack is unchanged. The newer programme map is included separately. Setup, sync
code, tests and workflow are maintenance material, not training content.

No credentials, actual employee/customer/participant records, adopted policies or fabricated
approvals are added. Do not infer disability, capability or authority from examples. Real
evidence handling requires appropriate purpose, permissions and protected records.

## Updates and checks

Manual runs and Mondays at 08:47 UTC are configured in GitHub. Schedules can be delayed or
disabled after public-repository inactivity. Publication is one-way from allow-listed,
committed GitHub sources. New/renamed sources and changed licences need explicit review.
Missing files/context, unsafe paths, private-access metadata or changed root/file-specific
licence declarations block publication. This is dataset publication, not legal monitoring.

Eight files are managed: README.md, LICENSE, NOTICE.md, documents.jsonl, knowledge_chunks.jsonl,
provenance.json, record_schema.json and validation_report.json. Existing unmanaged files,
including .gitattributes, and visibility are preserved; unmanaged content does not automatically
stay current and historical downloads are not recalled. Destination: `{target}`.

Checks establish faithful extraction, context, metadata, schema and checksums, not legal
currency, adopted policy, authentic authority, genuine evidence or operational effectiveness.
Verify authenticated publication in the workflow result and destination provenance/history;
pin a dataset revision for reproducible use.
'''
    yaml.safe_load(card.split('---',2)[1]);(output/'README.md').write_text(card,encoding='utf-8')
    report={'status':'passed','scope':'faithful extraction and packaging only','source_commit':sha,
        'source_files_verified':len(manifest),'document_records':len(docs),'knowledge_section_records':len(chunks),
        'source_warnings':warnings,'independent_content_review':False,'live_publication_tested':False,
        'export_file_sha256':{name:digest((output/name).read_bytes()) for name in MANAGED if name!='validation_report.json'}}
    write_json('validation_report.json',report);return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    print(json.dumps(build(ROOT,args.output)))

if __name__=='__main__':main()
