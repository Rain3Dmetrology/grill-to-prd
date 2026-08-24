# Third-Party Attributions

grill-to-PRD adapts portions of the following open-source projects. Each is
retained under its own license; the composite project (grill-to-PRD) is MIT.

## 1. mattpocock/skills — MIT License

- Source: https://github.com/mattpocock/skills
- Copyright (c) Matt Pocock
- Adapted components: `grilling` (design-tree / frontier interview loop),
  `grill-with-docs` (orchestration), `domain-modeling` (glossary + ADR triggers),
  `to-spec` (seams + spec template), `to-tickets` (tracer-bullet decomposition).
- Modifications: integrated into a dual-mode (Deep/Fast) router; added
  E0-E3 evidence grading, acceptance-gate (G1/G2/G3) mapping, and JSON+Markdown
  dual-form output. Modified files carry the required "changed" notices per
  license terms.

## 2. snarktank/ralph — MIT License

- Source: https://github.com/snarktank/ralph
- Copyright (c) snarktank
- Adapted components: `prd` skill (Lettered Options clarification + PRD template).
- Modifications: added evidence grading and acceptance-command-first rules.

## 3. huggingface/skills — Apache License 2.0

- Source: https://github.com/huggingface/skills
- Copyright (c) Hugging Face
- Adapted components: `huggingface-best` (benchmark-driven model selection,
  device parameter-budget filtering).
- Modifications: rewired to use the HF MCP toolset for evidence retrieval (E1)
  instead of raw curl; added trusted-domain allowlist.
- Apache-2.0 requires retention of the original license text and NOTICE
  attributions. The full Apache License 2.0 text is available at:
  https://www.apache.org/licenses/LICENSE-2.0

---

No credentials, tokens, or secrets are stored in this repository. All
third-party attribution is informational per the respective license terms.
