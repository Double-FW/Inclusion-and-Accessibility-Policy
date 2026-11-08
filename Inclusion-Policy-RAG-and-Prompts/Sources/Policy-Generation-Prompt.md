Purpose:
  Generate an organisational policy for {{org_name}} on {{policy_topic}} using retrieval-augmented generation (RAG).
  Primary authoritative source: GitHub repository https://github.com/Double-FW/Inclusion-and-Accessibility-Policy
  Requirements:
    - Must include relevant regulatory requirements and authoritative citations (laws, standards, e.g., WCAG, ADA, regional accessibility laws).
    - Must include the organisation's mission statement and brand values.
    - Must include links or documents for previously-made executive commitments (e.g., Valuable 500, Disability:In, other pledges).
    - Must include any available policy documents, guidance, or brand writing style guides.
    - Must produce a machine-readable policy object conforming to the repo's agent expectations (rules.metadata, rules.constraints).
    - Must provide provenance (source list + permalinks) and confidence for each substantive claim.
    - If any required artifact is missing from available retrieval results, list exactly which artifacts are missing and request them.

Inputs (placeholders - supply when calling):
  - {{org_name}}           : canonical organisation name
  - {{policy_id}}          : desired policy id (colon-separated namespace, e.g., org:accessibility:keyboard-navigation)
  - {{policy_title}}       : short title for the policy
  - {{policy_topic}}       : topic / scope (web, mobile, recruitment, procurement, workplace, etc.)
  - {{audience}}           : intended readers (legal, engineering, product, HR)
  - {{sources}}            : optional list of repo paths or URLs to prioritize in retrieval (default: search the repository)
  - {{regulatory_jurisdictions}} : list of jurisdictions to include (e.g., EU, UK, US, Australia)
  - {{brand_style_guide}}  : optional link or path to brand writing style guide (if omitted, search repo)
  - {{mission_statement}}  : optional mission text or path (if omitted, search repo)
  - {{executive_commitments}} : optional list of links or names (e.g., "Valuable 500", "Disability:In")

Retrieval instructions (for the retriever component):
  1. Search the repository Double-FW/Inclusion-and-Accessibility-Policy first; return matching files, their permalinks, and line ranges for every cited excerpt.
  2. Augment with external authoritative sources for regulatory requirements and named executive commitments:
     - For laws/standards: cite official sources (W3C, government pages, EU directives, national accessibility acts).
     - For commitments: find pages confirming participation/commitment (Valuable 500, Disability:In, press releases).
  3. For each retrieved document, return: title, author/publisher, URL (permalink or canonical URL), retrieval timestamp, and a short reason why this document is relevant.
  4. Redaction: redact PII before long-term storage; if PII appears in retrieved content, replace with canonical tokens (REDACTED_EMAIL, REDACTED_SSN, etc.) and include the original evidence path in a secure audit-only field.

Generation instructions (for the LLM synthesizer):
  A. Validate inputs:
     - Ensure {{policy_id}} follows colon-separated namespace.
     - Ensure version uses ISO date or semver.
     - If any of the required artifacts (regulatory requirements, mission statement, executive commitments, brand values, style guide) are not found, output a "missing_artifacts" list and stop; do not generate the final policy until missing artifacts are supplied.
  B. Produce two outputs: Human policy (Markdown) and Machine policy (JSON).
     1) Human policy (Markdown; max 2 pages):
        - Title: {{policy_title}}
        - Policy ID and Version (use ISO date)
        - Scope & audience
        - Executive summary (3 bullets)
        - Required actions (clear, actionable steps)
        - Roles & responsibilities
        - Enforcement & escalation (when enforcement is blocking vs. advisory)
        - Remediation timeline by severity (low/medium/high/critical)
        - References & evidence (numbered list with permalinks)
     2) Machine policy (JSON) - MUST follow this minimal structure:
        {
          "rules": {
            "metadata": {
              "id": "{{policy_id}}",
              "title": "{{policy_title}}",
              "version": "{{iso_date_or_semver}}",
              "status": "draft|active|deprecated",
              "scope": ["{{policy_topic}}"],
              "applies_to": ["..."]
            },
            "constraints": [
              {
                "id": "c01",
                "description": "Concise constraint statement.",
                "severity": "low|medium|high|critical",
                "enforcement": "warn|monitor|blocking",
                "evidence": ["url:...","repo:path@sha#L10-L20"]
              }
            ]
          },
          "references": [
            {"type":"wcag","id":"2.1.1","url":"https://..."},
            {"type":"law","jurisdiction":"UK","title":"Equality Act 2010","url":"https://..."}
          ],
          "provenance": {
            "retrieved_from": [
              {"source":"repo","path":"...","url":"...","sha":"...","excerpt_lines":"L10-L20"}
            ],
            "confidence": 0.0-1.0
          }
        }
     - Ensure constraints[].severity maps to remediation timelines and enforcement levels.
     - Validate that rules.metadata.status is one of (draft, active, deprecated).
     - Validate that rules.metadata.id is present and colon-separated.

C. Envelope & observability (for every message produced):
   - Attach a JSON "envelope" object at top-level with:
     {
       "message_id": "uuid-v4",
       "timestamp": "{{iso_timestamp}}",
       "agent_version": "{{agent_name}}@{{version}}",
       "audit_id": "uuid-v4",
       "confidence": 0.0-1.0
     }
   - Include "audit_event" JSON Lines entry for any enforcement/escalation recommendation using the AGENTS.md audit schema. Example:
     {
       "audit_id":"uuid-v4",
       "timestamp":"2026-10-12T12:34:56Z",
       "agent":{"name":"inclusion-agent","version":"1.0.0"},
       "action":"assessment|escalation|enforcement|remediation",
       "policy_id":"policy:...",
       "constraint_id":"c01",
       "resource":"https://...",
       "result":"non-compliant|compliant|partial",
       "evidence":["url:...","repo:path@sha#L..."],
       "actor":{"type":"agent","id":"inclusion-agent"}
     }

D. Citations & provenance:
   - Every factual claim about a regulation, commitment, or brand rule MUST include a citation with a permalink or canonical URL and a retrieval timestamp.
   - For repo sources, include the file path and line numbers and the commit SHA or branch used.

E. Safety, redaction, and privacy:
   - Do not include unreleased PII in outputs; redact as described above.
   - If a remediation requires contacting an individual, recommend role (e.g., "Data Protection Officer") rather than personal contact info.

F. Final checklist (must be included in output):
   - All required artifacts present? (yes/no). If no: list missing.
   - Machine policy JSON validated against minimal rules structure? (yes/no). If no: list validation errors.
   - List of all sources cited (with permalinks and retrieval timestamps).
   - Suggested next steps (assignments, timelines).

Behavior on missing or ambiguous inputs:
  - If mission statement, brand values or style guide are not present in the repo or inputs, request them explicitly and do NOT finalize the policy.
  - If regulatory scope ambiguous, ask to confirm jurisdictions.

Example invocation:
  - Call the retriever with "search repo Double-FW/Inclusion-and-Accessibility-Policy for 'mission', 'brand', 'style', 'commitment', 'Valuable 500', 'Disability:In', 'policy'".
  - Supply the top-5 repo matches as prioritized sources to the generator along with external regulatory links discovered.
  - Run the generator with placeholders filled and require a machine policy JSON and the envelope + audit_event.

Output expectations:
  - Top-level: envelope JSON, machine policy JSON, human policy Markdown, audit_event JSON Lines, provenance list, final checklist.
  - All URLs must be full permalinks (for repo: https://github.com/Double-FW/Inclusion-and-Accessibility-Policy/blob/<branch-or-sha>/path#L10-L20).
  - Confidence score per major section and an overall confidence for the policy.
