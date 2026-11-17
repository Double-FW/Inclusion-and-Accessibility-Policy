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
The repository includes [AGENTS.md](AGENTS.md), which provides governance guidance for source authority, evidence, uncertainty, privacy and human decision boundaries. It is an instruction document, not an implemented policy-rule schema, audit service, deployment or enforcement system. Generated policy remains a draft until the organisation's authorised people approve it.

AGENTS.md declares CC BY 4.0 in its front matter; the root LICENSE declares MIT. Retain the file-specific notice and attribution alongside the root licence when reusing the collection. External sources retain their own terms.

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

This prompt is most effective when used alongside `AGENTS.md` and `Accessibility_and_Inclusion_Policy_Creation_Guide.md`, which guide source traceability and human governance for drafting. The separate Policy-Generation-Prompt.md contains illustrative machine-policy and audit assumptions that the current AGENTS.md does not define or implement; use them only as proposals for local review.

## Purpose

The repository supports organisations in designing inclusion and accessibility policy that is both compliant and values-driven. It is intended to help translate principles into operational practice, strengthen accountability, and embed measurable inclusion outcomes in governance and delivery.

## Repository status

This repository acts as a working reference for inclusion and accessibility policy development, operational governance, and agent-assisted policy handling.


## Hugging Face dataset publication

The [Hugging Face dataset](https://huggingface.co/datasets/GarethFW/Disability_Inclusion_and_Accessibility_Policy) is published from the approved current sources. Follow the [complete setup and verification guide](huggingface/SETUP.md) for token creation, the GitHub secret, first run and weekly publication. The historical RAG/source snapshot pack is excluded to avoid duplication. Source prompts are retained as data and are never executed. Publication does not adopt an organisational policy, approve commitments or deploy the described governance controls. Dataset documentation preserves both MIT and file-specific CC BY 4.0 notices with attribution.
