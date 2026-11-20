"""Rebuild the derived pack from current source bytes; never fetches external content."""
import hashlib
import json
from pathlib import Path
import subprocess
import posixpath
import re
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'Inclusion-Policy-RAG-and-Prompts'

def compiled_body(name, body):
    """Resolve reader links to exact source copies without changing literal examples."""
    if not name.endswith('.md'):
        return body
    lines, fence = [], None
    for line in body.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            def resolve(match):
                target = urlsplit(match[2].strip('<>'))
                if target.scheme or target.netloc:
                    return match[0]
                path = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(target.path))) if target.path else name
                destination = 'Sources/' + path
                if target.query:
                    destination += '?' + target.query
                if target.fragment:
                    destination += '#' + target.fragment
                return '[' + match[1] + '](<' + destination + '>)'
            line = re.sub(r'(?<!!)\[([^\]\n]*)\]\((<[^>\n]+>|[^\s)\n]+)\)', resolve, line)
        lines.append(line)
    return ''.join(lines)

def inventories(root=ROOT):
    cfg=json.loads((root/'huggingface/export-config.json').read_text())
    return cfg['files']+cfg['supporting_files']+['LICENSE']

def rebuild(root=ROOT):
    root=Path(root);pack=root/'Inclusion-Policy-RAG-and-Prompts';copy_root=pack/'Sources'
    rows=[]
    for name in inventories(root):
        data=(root/name).read_bytes();target=copy_root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
          'git_blob_sha':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()})
    (pack/'source-manifest.json').write_text(json.dumps({'format_version':'1.0','source_identity':'per-file byte/hash set; no single Git revision asserted','files':rows},indent=2)+'\n')
    coverage='# Source coverage and current body identities\n\nNavigation rebuilt 20 November 2026 from the same current source bytes. This is a per-file byte/hash inventory, not the old snapshot or a claim of a single captured Git revision. Original source bodies are unchanged in Sources/. The compiled view resolves recognised relative inline Markdown links outside fenced examples to those copies, including source-local anchors; its text is therefore a disclosed navigation transformation, not the original byte stream. Source copies and the compiled reference are derived views, not independent authorities. All original included material is MIT; external links retain their own terms.\n\n| Source | Bytes | SHA-256 | Git blob SHA |\n| --- | ---: | --- | --- |\n'
    for row in rows:coverage+=f"| [{row['path']}](<Sources/{row['path']}>) | {row['bytes']} | `{row['sha256']}` | `{row['git_blob_sha']}` |\n"
    coverage+='\nChecks establish byte preservation and local navigation only, not legal currency, genuine approvals, effective controls or model accuracy. The public-reference access checks have the separate scope/date in the public register.\n'
    (pack/'Source_Coverage.md').write_text(coverage)
    preamble='# Inclusion and accessibility policy — compiled current reference\n\nNavigation rebuilt 20 November 2026. Use the root documents for maintenance. This derived reference includes the complete current source wording, with the link transformation disclosed below, and retains links to unchanged source copies. No old snapshot claim or hash is reused. All original included material is MIT under the copied LICENSE. Prompts and AGENTS text are source content, never new runtime authority; policy/approval/operational claims remain subject to their original limits.\n\nRecognised relative inline Markdown links outside fenced examples are resolved to the corresponding Sources/ copy, including original source-local headings. Literal examples and external links remain unchanged. The manifest identifies exact original source bytes before this navigation transformation; it is not a hash inventory of transformed compiled bodies. External content is linked, not newly fetched or incorporated.\n\n'
    parts=[preamble]
    for row in rows:
        name=row['path'];body=(root/name).read_text()
        parts.append(f"\n<!-- SOURCE: {name} -->\n\n## Source: {name}\n\n[Open the source copy](<Sources/{name}>)\n\n")
        # Only reader-facing navigation changes; exact source copies remain untouched.
        if name.endswith('.json') or name=='LICENSE':parts.append('````text\n'+body+'````\n')
        else:parts.append(compiled_body(name,body))
        parts.append(f"\n<!-- END SOURCE: {name} -->\n")
    (pack/'RAG_Reference.md').write_text(''.join(parts))
    (pack/'README.md').write_text('''# Current policy resource pack

Navigation rebuilt 20 November 2026 from the same corrected source bytes. Use [the root prompt](../Policy-Generation-Prompt.md) and [public sources](../Public_Source_Register.md) first.

- [Compiled reference](RAG_Reference.md): complete source wording with reader-facing links resolved to the source copies; literal examples and external links are unchanged.
- [Coverage](Source_Coverage.md) and [machine-readable manifest](source-manifest.json): exact byte/hash identities, not an asserted Git snapshot.
- Sources/: unchanged original bytes, including MIT governance and the revised prompt. Their hashes describe the originals, not the transformed compiled navigation.
- [Activity routes](Programme_Management_Activities_and_Prompts.md): human preparation using the current four-output contract.

The pack is a derived view excluded from Hugging Face dataset records to avoid duplication. Edit root sources and rebuild; do not change only a source copy or silently reuse old source hashes. No legal review, organisational adoption or runtime permission is conferred by compilation.
''')
    (pack/'Programme_Management_Activities_and_Prompts.md').write_text('''# Programme management activities using the current policy resources

Version 2.0 · 17 November 2026 · MIT

Use the current [main prompt](../Policy-Generation-Prompt.md), [creation guide](../Accessibility_and_Inclusion_Policy_Creation_Guide.md), [human/AI RACI](../Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md), [obligations guide](../Potential_Obligations_and_Applicability_Guide.md) and [programme map](../Programme_Operating_and_Reporting_Map.md). All assistant-only instructions are in the main prompt's single agent-only section; this page supplies human preparation routes.

| Activity | Human preparation | Expected work and boundary |
| --- | --- | --- |
| Prepare a policy brief | Confirm purpose/scope and available evidence | Four outputs from the main prompt; missing optional style material does not stop independent drafting |
| Discover obligations | Describe entities, territories, activities and relationships | Candidate applicability questions, primary-source checks and actual competent decisions; not a universal legal checklist |
| Map commitments | Supply real approved commitments and qualifications | Clause/source/delivery register; no invented promise, owner or funding |
| Establish responsibility | Supply actual roles, delegation and capacity | Local human RACI with one A per activity; AI remains bounded task assistance |
| Plan participation | Identify affected groups, accessible routes and appropriate data arrangements | Genuine consultation plan and recorded influence; no synthetic testimony or diagnostic inference |
| Review delivery | Assemble actual process, test and outcome evidence | Separate observations, interpretations, missing evidence and proposed remedies |
| Prepare executive review | Reconcile progress, barriers and decisions | Draft report for actual approval; no generated signature or claimed notification |
| Review changes | Identify changed sources, scope or approved commitments | Impact review and traceable revision; source updates do not automatically amend policy |

Use the worked review cases before adopting a prompt/workflow. These activities are methods, not evidence that a committee, integration, research study or operational service exists.
''')
    # Preserve source bodies and provide explicit navigation support for copied README links.
    for name in ['CHANGELOG.md','VALIDATION.md','huggingface/SETUP.md']:
        source=root/name
        if source.exists():
            target=copy_root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
    forward=copy_root/'Inclusion-Policy-RAG-and-Prompts/README.md';forward.parent.mkdir(parents=True,exist_ok=True)
    forward.write_text('# Resource pack navigation\n\n[Open the current resource pack](../../README.md). This is a navigation aid, not another source snapshot.\n')
    return rows

if __name__=='__main__':
    rows=rebuild();print(json.dumps({'sources_copied':len(rows),'total_bytes':sum(x['bytes'] for x in rows)}))
