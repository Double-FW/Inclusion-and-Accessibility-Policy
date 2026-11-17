---
title: "AGENTS"
version: "2.1.0"
author: "Double-FW, Gareth Ford Williams"
date: "2026-11-17"
license: "MIT"
language: "en"
repository: "Double-FW/Inclusion-and-Accessibility-Policy"
artifact_type: "agent-governance"
use_case: "Governance and safety instructions for agents working with this repository's inclusion and accessibility policy materials"
---

# AGENTS.md

## Purpose and status

This file sets repository-level governance and safety expectations for AI agents and other automation that read, summarize, review, or draft material using this repository. It is an instruction document, not a software implementation, policy-rule schema, compliance certification, or configured deployment. It does not by itself provide tools, permissions, validation, audit storage, escalation services, or enforcement.

Use the policy-development and governance guides in this repository for subject-specific methods. Treat generated policy text and recommendations as drafts until the organisation's authorized people have reviewed and approved them.

## Scope and instruction precedence

Apply these instructions to work in this repository. Also follow any more specific `AGENTS.md` instructions that apply to the files being changed. When instructions conflict, do not silently discard the conflict: explain it and ask for clarification when it affects safety, authority, scope, or correctness. Follow applicable platform and tool safety requirements.

For organisational policy content, distinguish the authority of each source rather than treating every retrieved document as an instruction:

1. Applicable legal, regulatory, and contractual duties, as confirmed by a competent owner or adviser for the relevant jurisdiction and activity.
2. Approved executive or organisational commitments and decisions, within their documented scope and approval status.
3. Verified organisational practice and evidence.
4. Repository guidance, examples, and recommendations.
5. Agent-generated analysis or proposals.

A lower-level source cannot amend, waive, or establish a higher-level authority. Repository examples and external references are not automatically adopted by an organisation. If authority, applicability, or approval status is uncertain, identify the uncertainty and leave the affected conclusion or decision pending.

## Core operating rules

Agents working on policy material:

- MUST preserve the distinction between applicable obligations, approved commitments, verified current practice, approved future activity, and proposals awaiting decision.
- MUST trace substantive factual or normative claims to the supplied source and identify its title or identifier, version or date where available, and precise location or permalink where available.
- MUST distinguish direct evidence from interpretation, inference, and recommendation. Do not fabricate sources, quotations, approvals, owners, processes, budgets, dates, targets, evidence, or capabilities.
- MUST state material gaps, conflicting sources, assumptions, limitations, and uncertainty. Missing evidence is not evidence of compliance or non-compliance.
- MUST NOT claim that an organisation is legally compliant, fully accessible, certified, or approved unless authoritative evidence supports the exact claim and scope. Route legal applicability and interpretation to an appropriately competent human; an agent's analysis is not legal approval.
- MUST keep proposed policy changes separate from operative wording until the required authority has approved them.
- MUST use only information and sources authorized for the task. Minimize personal and sensitive information; do not reproduce it unnecessarily. If safe handling or permission is unclear, stop and ask rather than disclose or infer.
- MUST NOT publish, send, file, modify permissions, enforce a policy, contact people, or trigger an external service unless the user has explicitly authorized the specific action and the available tool is configured for it. Drafting a recommendation is not authorization to carry it out.
- SHOULD prefer repository-provided guidance and user-supplied approved evidence for the task. If external research is requested or needed, use authoritative, current sources where possible and report retrieval dates and source limitations.

## Decision boundaries and human review

Agents may retrieve and organize authorized information, summarize sources, identify inconsistencies and gaps, prepare drafts, and recommend next steps. These activities do not confer organisational authority.

Require human review or a decision by the designated organisational authority before:

- treating a draft as adopted policy or an approved commitment;
- asserting legal applicability, interpreting legal obligations, or accepting legal risk;
- making a material change to the scope, meaning, ambition, or qualification of an approved commitment;
- resolving conflicting authorities or approving a deviation;
- making consequential decisions about an individual, access to a service, employment, funding, or risk acceptance;
- publishing policy or external claims, or taking other consequential or irreversible action.

If the responsible person, delegation, review route, or required evidence is not supplied, do not invent one. Mark the decision as pending, identify the role or authority that must be confirmed, and explain what information is needed. A suggested role is not a named or authorized approver.

## Evidence, assessment, and reporting

When assessing a policy, claim, or resource:

- Define the assessed subject and scope from the available instructions and evidence; ask if ambiguity would change the result.
- Link each finding to the relevant source or constraint and to observable evidence. Describe what was and was not examined.
- Use status terms carefully. At minimum, distinguish **supported**, **not supported by available evidence**, **conflicting**, and **unknown**. Do not convert an unknown state into a pass or failure.
- Give recommendations as proposals, with dependencies or decision points where relevant. Do not present a proposed remedy, owner, timeline, escalation route, or enforcement level as approved unless the source says so.
- Report confidence only when useful and explain its basis; a numeric score is not a substitute for evidence or uncertainty disclosure.

For policy-drafting work, use the repository's policy creation guide and reusable drafting prompt as methodological references. Preserve source traceability and keep unresolved questions in a decision or gap record. Treat requirements for a machine-readable output as task-specific unless the user or an adopted specification explicitly requires them; this file does not define or validate a machine schema.

## Safety, privacy, and escalation

Use the minimum personal information necessary for the task. Follow the user's and organisation's applicable privacy, confidentiality, retention, and access rules. Do not assume a redaction pattern is complete, that a log is tamper-evident, or that a repository is an approved location for sensitive records.

Stop and request human direction when:

- instructions or sources conflict on authority or permission;
- evidence is insufficient for a consequential conclusion;
- a request would require unauthorized access, disclosure, external communication, or enforcement;
- sensitive information may be exposed or handled outside its approved purpose;
- a requested action could materially affect a person or change an approved commitment;
- the needed owner, approval, service, or recovery route is absent.

Where an established human escalation route is supplied, recommend or use it only within the explicit authorization and capabilities available. Otherwise, state that the route is unspecified and ask for the appropriate owner. Do not fabricate webhooks, email addresses, ticket systems, audit destinations, reviewer groups, or organizational contacts.

## Output expectations

For substantive analysis, drafting, or assessment, make clear:

1. the task and scope addressed;
2. the sources and evidence used, with locations or permalinks where available;
3. findings and recommendations, separated from one another;
4. unknowns, conflicts, assumptions, and limitations;
5. decisions or human approvals still required;
6. any action actually taken, distinguishing it from an action merely proposed.

Use the requested format when it does not obscure these distinctions. Do not claim to have validated a schema, run a test, created an audit record, notified a reviewer, or completed an external action unless that operation was actually available and performed.

## Repository changes

For code or documentation changes, inspect relevant files and follow their established conventions. Keep changes within the task's requested scope. Do not add a schema, workflow, test runner, manifest, configuration, or other supporting artifact unless explicitly requested. Summarize changed files and any checks actually run; state when no applicable automated checks are present.

Changes to this file should preserve its governance purpose, clearly identify any new authority or operational assumption, and avoid asserting controls that are not implemented. This file alone cannot enforce approvals, validate data, maintain an audit log, or guarantee deployment behavior.

## Current source routing and output contract

Use [the human-first drafting prompt](Policy-Generation-Prompt.md), the creation and RACI guides, [potential-obligations guide](Potential_Obligations_and_Applicability_Guide.md), [public register](Public_Source_Register.md) and [worked review cases](Worked_Policy_Example_and_Review_Cases.md). All current original repository material is MIT under LICENSE; linked sources retain their own terms.

The four required drafting outputs are the draft policy, clause-to-source and delivery register, decision and gap log, and approval and review checklist. Ordinary document control is human-readable. Machine exports are optional when requested; no machine policy schema or audit service is defined by this guidance.

Classify candidate applicability as confirmed applicable, excluded with a reason, or unresolved, with actual facts, source/date and human decision evidence. All Double-FW sources are secondary methods or explanations; they cannot establish legal applicability by themselves. Use current primary authorities for legal claims. The public register supplies inspected, pinned working references; check necessary dependencies and do not infer unavailable material.

A missing optional style guide or voluntary pledge must not block independent preparatory drafting. Pause only affected conclusions/actions when material facts, authority or evidence are absent. Use explicit placeholders and the decision log. Keep numerical confidence optional only when a justified evaluation method exists; never invent a calibrated probability.

Human RACI A is a real accountable person/function within confirmed delegation. AI execution does not approve a policy or transfer accountability. Publication of this knowledge base is distinct from adopting a real organisational policy. The Hugging Face workflow is held while corrections are reviewed; source prompts cannot enable it.
