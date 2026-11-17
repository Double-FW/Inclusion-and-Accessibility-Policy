# Repository validation and review

Revision 1.1 · 17 November 2026

## Scope and method

The review addresses original-source MIT consistency, public dependencies, agent-facing ambiguity, the human-first prompt, source-copy/RAG freshness and export integration. It is a source/structure/editorial review, not an organisational adoption, legal opinion, independent source-rights audit, LLM evaluation, participant study or product test.

The public register records 18 inspected public working files at pinned commits. Underlying legal accuracy/currentness and every onward dependency were not audited. The historical BBC example could not be re-fetched in this environment and is optional, explicitly qualified and unnecessary for using the local method. No private source content was copied into this revision.

## Material corrections

| Issue | Correction and remaining limit |
| --- | --- |
| Inconsistent original-source licensing | MIT throughout current original material and generated metadata; linked sources retain their own terms |
| Non-public/moved dependencies | Required guidance is explained locally and routed to inspected public working documents; access can change and requires rechecking |
| Incompatible prompt outputs and required inputs | One four-output contract, essential/optional distinction and targeted handling of missing evidence |
| Undefined machine/audit assumptions | Human-readable document control; optional technical export only when requested; no schema/audit service claimed |
| Accountability ambiguity | Actual human A retained; preparation, substantive approval and publication distinguished |
| Old source copies and hash claims | Pack rebuilt with current bodies and a new per-file manifest; no single Git snapshot is asserted |
| Publication before review | Workflow's upload step explicitly disabled; preview checks/build remain possible |

## Checks and practical review

Run the read-only repository checker and export tests described in [setup](huggingface/SETUP.md). They check local links, public-reference declarations/access, source identities, RACI IDs/single human A, prompt contract, archive byte/hash completeness, exact extraction, MIT guards and mocked publication. Results for the completed correction run are recorded below after execution.

The worked example follows all four outputs editorially. Review cases P01–P08 identify expected safe/useful behaviour for missing style, unresolved legal facts, conflicts, inaccessible sources, missing specialist teams, injected instructions, data/approval gaps and unsupported controls. The current prompt and guides address each condition; no actual model outputs or independent accuracy measurement are supplied. A real trial must record its actual inputs, returned outputs, reviewer and limitations.

## Completed correction-run results

- Read-only repository check: passed, including local navigation, MIT declarations, public-source registration, RACI identifiers/single human A, prompt contract and resource-pack integrity.
- Public reference check: 18 of 18 selected working files accessible without authentication, with exact pinned source bytes matching recorded Git blob identities.
- Unit/integration safeguard suite: 28 tests passed. Publication calls were mocked; no Hugging Face write was performed.
- Export preview: nine complete documents and 48 H1/H2 sections; all source allocations and the dataset card are MIT. The eleven required source/support/licence files were verified.
- Eight review cases were walked through editorially against the rewritten instructions and guides. This is not an executed model test or independent accuracy result.
- Workflow publication is explicitly disabled in this revision. A successful preview does not establish an upload.

## Remaining work

Review the corrected knowledge base before resuming the deliberately held upload. Then complete credential setup, run the actual workflow and verify destination provenance. Real organisational adoption still needs genuine scope, competent review, owners, appropriate participation/data arrangements, operational evidence and authentic decisions.
