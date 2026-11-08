# Inclusion-and-Accessibility-Policy

An Approach to generating organisational policies that align with regulatory frameworks as well as executive commitments and organisational values.

## Repository overview

This repository provides a structured, practical set of materials for developing and governing inclusion and accessibility policy in an organisation. It brings together:

- policy creation guidance
- governance and accountability structures
- operational decision-making patterns
- agent rules and automation metadata
- licensing and usage terms

## Contents

### 1. AGENTS.md
The repository includes `AGENTS.md`, which defines machine-readable operational rules for automated agents, including:
- YAML/JSON policy metadata
- short prompt and response templates
- observability and audit logging requirements
- escalation and redaction rules
- quick-start checklist and decision flowgraph
- versioning, changelog, and review metadata

This file is intended to help automation work consistently and safely when preparing or reviewing inclusion and accessibility policy content.

### 2. Accessibility and Inclusion Policy Creation Guide
The main policy-development guide is:
- `Accessibility_and_Inclusion_Policy_Creation_Guide.md`

This document provides the core methodology for generating organisational policies that:
- align with regulatory frameworks
- reflect executive commitments
- express organisational values
- support practical implementation and measurable outcomes

### 3. RACI and Steering Group Guide
The repository also includes governance material for role clarity and oversight:
- `Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md`

This guide covers:
- roles and responsibilities
- RACI-style accountability mapping
- steering group composition and function
- decision-making responsibilities for policy ownership and monitoring

### 4. License
The repository is distributed under the terms in:
- `LICENSE`

### 5. Documentation map

This repository is organised as a policy and governance knowledge base containing:
- policy generation methodology
- governance implementation guidance
- automation metadata and operational guardrails
- legal and licensing information

## Recommended starting points

If you are new to this repository, begin with:
1. `AGENTS.md` for automation and operational guidance
2. `Accessibility_and_Inclusion_Policy_Creation_Guide.md` for policy drafting methodology
3. `Accessibility_and_Inclusion_Policy_RACI_and_Steering_Group_Guide.md` for governance and accountability structure
4. `LICENSE` for usage terms

## Policy generation prompt overview

This repository includes a reusable prompt for generating an organisational accessibility and inclusion policy from evidence, approved commitments, and governance context. The prompt is designed for a policy author, delegated governance lead, or AI-assisted drafting workflow. It is a drafting aid, not an authority to change organisational obligations or commitments.

The purpose of the prompt is to produce a policy draft that:
- reflects the organisation's mission, values, and approved commitments
- aligns with applicable legal and regulatory duties
- identifies the scope, decision owners, and evidence basis for each clause
- distinguishes approved commitments from future intentions or unverified proposals
- captures unresolved gaps or conflicts for human review before approval

### Prompt inputs

Provide the prompt with the following information:
- organisation name and context
- approved executive commitments
- regulatory or contractual obligations that apply to the organisation
- brand values, purpose, and strategic intent
- operational activities, service journeys, and affected stakeholders
- current governance, ownership, and delivery processes
- evidence from research, testing, complaints, participation, and operational records
- any known gaps, conflicts, or unresolved questions

### Prompt instructions

Use the following instruction pattern when generating a draft policy:

```text
Create a draft accessibility and inclusion policy for [organisation].
Use the supplied approved commitments, validated applicability register, brand values,
activity and journey inventory, current governance processes, and evidence pack.
Reflect the organisation's own vocabulary, scope, and decision authority.
Trace every substantive clause to its source identifier and preserve the approval status
of each commitment or obligation.

Connect each commitment to an intended outcome, relevant activity, process,
accountable owner, evidence, reporting route, and review trigger.
Do not invent legal conclusions, ownership, budgets, deadlines, certification claims,
resource commitments, or delivery capabilities without evidence.
Where information is missing, use a clearly marked placeholder and record the question for review.
Identify conflicts, gaps, and approval questions, and state which authority should decide them.

Return four outputs:
1. the draft policy
2. a clause-to-source and delivery register
3. a decision and gap log
4. an approval and review checklist

Clearly identify which material is ready for review and which elements require executive,
legal, or operational confirmation before adoption.
```

### Output requirements

The generated output should include:
- a policy draft with clear sections for purpose, scope, commitments, delivery, ownership, evidence, and review
- clause-level traceability from each policy statement to its authority or evidence source
- a decision log for conflicts, missing authority, and unresolved implementation gaps
- an approval checklist confirming ownership, validation, and review readiness

### Mandatory safeguards

Before the draft is considered usable for formal adoption, the organisation must:
- confirm the source authority for each material clause
- validate all stated legal or regulatory obligations
- verify ownership, reporting, and escalation responsibilities
- check that approved commitments are not overstated or conflated with aspirational intent
- review participation evidence and unresolved barriers with affected stakeholders

This prompt is most effective when used alongside `AGENTS.md` and `Accessibility_and_Inclusion_Policy_Creation_Guide.md`, which define the governance, audit, and automation expectations for policy drafting.

## Purpose

The repository supports organisations in designing inclusion and accessibility policy that is both compliant and values-driven. It is intended to help translate principles into operational practice, strengthen accountability, and embed measurable inclusion outcomes in governance and delivery.

## Repository status

This repository acts as a working reference for inclusion and accessibility policy development, operational governance, and agent-assisted policy handling.
