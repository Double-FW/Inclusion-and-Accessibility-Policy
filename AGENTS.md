---
title: "AGENTS"
version: "1.0.0"
author: "Double-FW"
date: "2026-10-12"
license: "CC-BY-4.0"
language: "en"
repository: "Double-FW/Inclusion-and-Accessibility-Policy"
artifact_type: "agent_spec"
use_case: "Automated assistance for generating and enforcing organisational inclusion & accessibility policies"
entities:
  - Policy
  - RegulatoryFramework
  - ExecutiveCommitment
  - OrganisationalValue
  - Escalation
  - AgentAction
  - DecisionNode
  - Evidence
  - Reviewer
---

# AGENTS.md

This file defines machine-readable rules, templates, observability requirements, and a minimal programmatic decision flow for any automation (agent) that consumes, proposes, or enforces organisational inclusion and accessibility policies in this repository.

## 1. Machine-readable rules and metadata

All rules MUST be provided in either YAML or JSON objects under clearly named keys. Agents MUST parse `rules.metadata` and `rules.constraints` keys before applying any action.

Example canonical structure (YAML):

```yaml
rules:
  metadata:
    id: "policy:accessibility:keyboard-navigation"
    title: "Keyboard navigation requirement"
    version: "2026-10-12"
    status: "active" # active | draft | deprecated
    scope: ["web", "mobile"]
    applies_to: ["public-website", "internal-dashboard"]
  constraints:
    - id: "c01"
      description: "All interactive controls MUST be reachable by keyboard"
      severity: "high"
      enforcement: "blocking"
  references:
    - type: "wcag"
      id: "2.1.1"
      url: "https://www.w3.org/TR/WCAG21/"
```

JSON example (same structure):

```json
{
  "rules": {
    "metadata": {
      "id": "policy:alt-text",
      "title": "Alternative Text for Images",
      "version": "2026-10-12",
      "status": "active"
    },
    "constraints": [
      {"id": "c01", "description": "All meaningful images MUST have alt text", "severity": "high"}
    ]
  }
}
```

Schema requirements (agents must validate before action):
- rules.metadata.id (string, colon-separated namespace)
- rules.metadata.version (ISO date or semver)
- rules.metadata.status (one of: draft, active, deprecated)
- constraints[].id (string)
- constraints[].description (string)
- constraints[].severity (low|medium|high|critical)
- enforcement (optional; warn|monitor|blocking)

Store canonical JSON Schema at `.github/agent-schemas/policy-rule.schema.json` (recommended).

## 2. Prompt/response templates (short, templated examples)

These templates are intentionally compact to be used by language-model-based agents for consistent outputs.

Prompts the agent can receive (templated):
- "Summarize policy {{policy_id}} in 3 bullets."
- "Assess compliance of resource {{resource_url}} against {{policy_id}}."
- "Propose remediation steps for constraint {{constraint_id}} with severity {{severity}}."

Example agent responses (templates):

Template: summary (JSON):

```json
{
  "policy_id": "{{policy_id}}",
  "summary": ["bullet1","bullet2","bullet3"],
  "confidence": "0.85"
}
```

Template: assessment output (YAML):

```yaml
assessment:
  policy_id: "{{policy_id}}"
  resource: "{{resource_url}}"
  result: "non-compliant" # compliant | non-compliant | unknown
  findings:
    - id: "f-001"
      constraint_id: "c01"
      description: "Control X not reachable by keyboard"
      evidence: "screenshot:sha256:... | url:..."
  remediation:
    - "Add tabindex and keyboard handlers"
  score: 0.34
  generated_at: "{{iso_timestamp}}"
```

Short, repeatable reply template for confirmations:
- "Action: {{action}} — Policy: {{policy_id}} — Outcome: {{outcome}} — AuditRef: {{audit_id}}"

Agents should expose a machine-readable 'envelope' on every message that includes `message_id`, `timestamp`, `agent_version`, and `audit_id`.

## 3. Observability hooks and logging requirements

Every escalation or enforcement action MUST emit a structured audit event with the following minimum schema (JSON Lines preferred):

Audit event schema (JSON):

```json
{
  "audit_id": "uuid-v4",
  "timestamp": "2026-10-12T12:34:56Z",
  "agent": {"name": "inclusion-agent", "version": "1.0.0"},
  "action": "escalation|enforcement|assessment|remediation",
  "policy_id": "policy:...",
  "constraint_id": "c01",
  "resource": "https://...",
  "result": "non-compliant|compliant|partial",
  "evidence": ["url:...","s3://bucket/path"],
  "actor": {"type":"agent|user","id":"..."}
}
```

Logging and retention requirements:
- All audit events MUST be written to a tamper-evident log (append-only) and forwarded to the organisation's centralized logging (e.g., SIEM) within 1 minute.
- Retention: store full audit events for 7 years unless policy/regulator specifies otherwise; store summarized indices for 10 years.
- Access controls: only authorised reviewers (role-based) can access raw events.

Redaction rules (when presenting or exporting logs):
- Personal Identifiable Information (PII) MUST be redacted prior to long-term archival or cross-team sharing. Use these canonical redaction rules:
  - Email: redact by regex ([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}) -> "REDACTED_EMAIL"
  - SSN/NIN: detect by pattern -> "REDACTED_SSN"
  - Secrets (API keys, tokens): detect via key patterns (e.g., AKIA..., xoxp-..., token=) -> "REDACTED_SECRET"
- Redaction MUST be reversible only to authorised auditors via a separate key-wrapped store if required for legal investigation.

Escalation hooks (mandatory):
- webhook: POST /internal/escalations with payload=AuditEvent
- email: send to security-accessibility@company.example with subject "Escalation: {{policy_id}} {{resource}}"
- ticket: open in tracker with fields: {policy_id, severity, evidence_refs, owner_suggested}

## 4. Quick-start checklist & minimal decision flowgraph

Quick-start checklist (for operators and for the agent to validate environment):
- [ ] Agent has read access to repository policies and `.github/agent-schemas/`.
- [ ] Agent has write access to `logs/audit/` or to the organisation's logging endpoint.
- [ ] Agent identity and credentials provisioned and rotated per org policy.
- [ ] Retention and redaction config present at `config/observability.yaml`.
- [ ] Reviewers list present at `OWNERS` and `POLICY-REVIEWERS`.

Minimal decision flowgraph (YAML, nodes & transitions):

```yaml
flowgraph:
  start: "ingest_policy"
  nodes:
    - id: "ingest_policy"
      type: "action"
      action: "validate_schema"
      on_success: "assess_resource"
      on_failure: "raise_schema_error"
    - id: "assess_resource"
      type: "action"
      action: "run_assessment"
      on_success: "evaluate_result"
      on_failure: "log_and_retry"
    - id: "evaluate_result"
      type: "decision"
      decision:
        - condition: "result == compliant"
          next: "acknowledge"
        - condition: "result == non-compliant and severity in [high,critical]"
          next: "escalate"
        - condition: "result == non-compliant and severity in [low,medium]"
          next: "propose_remediation"
    - id: "propose_remediation"
      type: "action"
      action: "create_remediation_proposal"
      on_success: "acknowledge"
    - id: "escalate"
      type: "action"
      action: "emit_audit_and_escalate"
      on_success: "acknowledge"
    - id: "acknowledge"
      type: "terminal"
      outcome: "complete"
    - id: "raise_schema_error"
      type: "action"
      action: "emit_schema_error_audit"
      on_success: "acknowledge"
    - id: "log_and_retry"
      type: "action"
      action: "emit_transient_error_and_retry"
      on_success: "assess_resource"

```

Programmatic guidance:
- All 'action' nodes must return an object: {status: "ok"|"failed", details: {...}, audit_id: uuid}
- Decision nodes evaluate against the `result` and `severity` fields returned by previous action.

## 5. Version, changelog, and review metadata

Machine-checkable metadata block (at repo path: `.github/agents/AGENTS.metadata.yaml` recommended):

```yaml
version: "1.0.0"
changelog:
  - version: "1.0.0"
    date: "2026-10-12"
    changes:
      - "Initial AGENTS.md with machine-readable rules, templates, observability, and flowgraph"
reviews:
  last_reviewed_by: "Double-FW"
  last_reviewed_at: "2026-10-12"
  review_status: "approved"
  review_notes: "Initial commit. Follow-up: add JSON Schema file and map to specific regulatory frameworks."
trust_requirements:
  - require_schema_validation: true
  - require_review_status: "approved"
  - require_version_match: true
```

Automation checks before trusting rules (examples):
- Confirm `trust_requirements.require_schema_validation` is true and `.github/agent-schemas/policy-rule.schema.json` exists and validates the policy document.
- Confirm `reviews.review_status == approved` and `last_reviewed_at` within 365 days.
- Confirm version in the policy `rules.metadata.version` matches `version` above or is <= current.

## 6. Governance and reviewer process (brief)

- Any change to `AGENTS.md`, `.github/agent-schemas/`, or `config/observability.yaml` requires: a) a pull request, b) at least two reviewers from `POLICY-REVIEWERS`, c) a passing CI validation that runs schema checks.
- Minor editorial changes MAY be fast-tracked if reviewers listed in `OWNERS` grant explicit approval.

## Appendix: Useful snippets

- Example audit event emission (pseudo-HTTP):

POST /internal/escalations
Content-Type: application/json

{ "audit_id": "...", "policy_id": "...", "details": { ... } }

- Minimal retention config example (`config/observability.yaml`):

```yaml
observability:
  audit_log:
    transport: "s3"
    bucket: "org-audit-logs"
    prefix: "inclusion-agent/"
    retention_days: 2555 # ~7 years
  redaction:
    enabled: true
    rules:
      - name: "email"
        regex: "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
        replacement: "REDACTED_EMAIL"
```

---

If you want, I can also:
- Add a JSON Schema file under `.github/agent-schemas/` to validate `rules` documents.
- Create a sample `POLICY-EXAMPLE.yaml` following the schema.

