# PRD Intake → Harness LOOP：字段映射与职责边界

> Status: integration guidance for GACP v2.2.1. This document is not a second normative control specification.

## Authority

- Requirements elicitation and PRD authoring: `grill-to-prd`.
- Execution contract, lifecycle, risk, permissions, approvals, budgets, evidence validity, Effect Journal, recovery and closure: [Harness LOOP Specification v3.1.1](https://github.com/Rain3Dmetrology/agent-harness-loop-spec/blob/84e74b98e628a9358765a261e281fb474018a686/SPEC.zh-CN.md).
- The Harness repository currently labels implementation attestation `UNATTESTED`; this mapping does not claim that a local deployment has C1/C2 controls.

## Mapping

| PRD artifact | Downstream Harness concept | Rule |
|---|---|---|
| `goal.purpose` | `TaskContract.objective` | Preserve user intent; do not silently rewrite it. |
| `goal.in_scope/out_of_scope` | `TaskContract.scope` | Scope changes require a new authorized contract version. |
| `requirements`, `user_stories` | Deliverables and acceptance predicates | Convert each relevant requirement into a specific predicate; do not copy all narrative into runtime context. |
| `acceptance[]` | `TaskContract.acceptance[]` | Preserve predicate, expected result, verification method, gate and limitations. PRD labels are not proof of execution. |
| `facts[]` | Context/evidence references | Preserve source, retrieval time and limitations. A PRD fact is not by itself an EV-01 Evidence Record. |
| `assumptions[]`, `open_questions[]` | Contract assumptions and unknowns | Blocking unknowns must be resolved or explicitly accepted in the contract before READY. |
| `decisions[]`, `adrs[]` | Decision records / contract rationale | Human-owned decisions remain with the user; an ADR does not grant execution permission. |
| `acceptance.kind=human_acceptance` + `gate=closure` | Human closure predicate | Human acceptance is separate from technical, deterministic or physical verification. |
| `data_objects`, `pipeline_constraints`, `error_personality` | Optional architecture/runtime inputs | Include only when they materially reduce downstream ambiguity. |

## State and permission separation

1. `draft` means the requirement artifact can be reviewed while known unknowns remain.
2. `ready_for_plan` means the user has confirmed shared understanding and no blocking questions remain. It is **not** plan approval, TaskContract authorization, or permission to write to external systems.
3. Plan freeze and TaskContract versioning belong to the Orchestrator.
4. R2/R3 effects, credential use, external writes and irreversible actions must use the applicable Runtime/CAP/APR/FX controls. Skill text and PRD confirmation cannot substitute for them.
5. `verification` and `closure` are the Harness gate values. Do not recreate a fixed G1/G2/G3 ladder or an E0-E3 evidence scale in this Skill.

## Evidence and source allowlists

Domain adapter source lists express source suitability for fact retrieval only. They are not network egress allowlists, vendor approvals, security certifications or permission grants. Runtime and organization policy remain authoritative for tools, network access, secrets and external effects.

## Minimal conversion checklist

- [ ] Preserve scope and user intent.
- [ ] Convert applicable acceptance statements into explicit predicates with sensors/methods and expected results.
- [ ] Record unresolved assumptions and blocking questions.
- [ ] Bind current policies, risk, permissions, budgets and authority map in the Harness; do not infer them from the PRD.
- [ ] Keep human acceptance as a closure predicate, separate from technical verification.
- [ ] Retain PRD provenance and version/hash as artifact references.
