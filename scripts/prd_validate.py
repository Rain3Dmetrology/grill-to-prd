#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate grill-to-PRD JSON artifacts.

This deterministic checker is not a quality score, security approval, or
Harness conformance test. It uses Python's standard library and validates the
small JSON Schema keyword profile used by templates/prd-schema.json:
type, const, enum, required, properties, additionalProperties, items,
minItems and minLength. Downstream consumers may run a full Draft 2020-12
validator independently.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SUPPORTED_SCHEMA_KEYS = {
    "$schema", "$id", "title", "description", "type", "required",
    "properties", "additionalProperties", "items", "minItems",
    "minLength", "enum", "const"
}
COLLECTIONS = (
    "acceptance", "facts", "assumptions", "decisions", "user_stories",
    "adrs", "open_questions", "data_objects", "pipeline_constraints",
    "error_personality"
)


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"unsupported JSON Schema type: {expected}")


def validate_schema_profile(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYS
    if unknown:
        raise ValueError(f"unsupported schema keyword(s) at {path}: {', '.join(sorted(unknown))}")
    expected = schema.get("type")
    if expected and not _type_matches(value, expected):
        return [f"{path}: expected {expected}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: must be one of {schema['enum']!r}")
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{path}: string shorter than minLength={schema['minLength']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: requires at least {schema['minItems']} item(s)")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(validate_schema_profile(item, item_schema, f"{path}[{index}]"))
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required property missing")
        properties = schema.get("properties", {})
        for key, child in properties.items():
            if key in value:
                errors.extend(validate_schema_profile(value[key], child, f"{path}.{key}"))
        if schema.get("additionalProperties") is False:
            for key in sorted(set(value) - set(properties)):
                errors.append(f"{path}.{key}: additional property not allowed")
    return errors


def semantic_errors(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for name in COLLECTIONS:
        values = doc.get(name, [])
        if not isinstance(values, list):
            continue  # the structural validator reports the type mismatch
        seen: set[str] = set()
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id:
                continue
            if item_id in seen:
                errors.append(f"$.{name}[{index}].id: duplicate ID {item_id!r}")
            seen.add(item_id)

    acceptance = doc.get("acceptance", [])
    if isinstance(acceptance, list):
        for index, item in enumerate(acceptance):
            if isinstance(item, dict) and item.get("kind") == "human_acceptance" and item.get("gate") != "closure":
                errors.append(f"$.acceptance[{index}]: human_acceptance must use gate='closure'")

    if doc.get("status") == "ready_for_plan":
        confirmation = doc.get("user_confirmation", {})
        if not isinstance(confirmation, dict) or confirmation.get("consensus_confirmed") is not True:
            errors.append("$.user_confirmation.consensus_confirmed: must be true for ready_for_plan")
        questions = doc.get("open_questions", [])
        blockers = [
            q.get("id", f"index-{i}")
            for i, q in enumerate(questions if isinstance(questions, list) else [])
            if isinstance(q, dict) and q.get("blocking") is True and q.get("status") == "open"
        ]
        if blockers:
            errors.append("$.open_questions: blocking questions remain open: " + ", ".join(blockers))

    adrs = doc.get("adrs", [])
    if isinstance(adrs, list):
        for index, adr in enumerate(adrs):
            if not isinstance(adr, dict) or adr.get("status") != "accepted":
                continue
            alternatives = adr.get("alternatives", [])
            if not isinstance(alternatives, list) or len(alternatives) < 2:
                errors.append(f"$.adrs[{index}].alternatives: accepted ADR requires at least two considered alternatives")
    return errors


def quality_warnings(doc: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    goal = doc.get("goal", {})
    success = goal.get("success_criteria", []) if isinstance(goal, dict) else []
    acceptance = doc.get("acceptance", [])
    facts = doc.get("facts", [])
    vague_terms = ("尽快", "尽量", "足够快", "体验好", "工作正常", "符合预期")
    texts = []
    for item in success:
        if isinstance(item, dict):
            texts.append(item.get("statement", ""))
    for item in acceptance:
        if isinstance(item, dict):
            texts.extend([item.get("statement", ""), item.get("expected_result", "")])
    if any(any(term in text for term in vague_terms) for text in texts):
        warnings.append("Replace vague success/acceptance wording with an observable result or measurement.")
    if not success:
        warnings.append("No explicit success_criteria were supplied; confirm acceptance adequately represents the goal.")
    for fact in facts:
        if isinstance(fact, dict) and fact.get("status") == "observed":
            source = fact.get("source", {})
            if not isinstance(source, dict) or not source.get("uri"):
                warnings.append("An observed fact has no source URI; add provenance or downgrade its status.")
                break
    stories = doc.get("user_stories", [])
    if stories and any(isinstance(s, dict) and not isinstance(s.get("invest"), dict) for s in stories):
        warnings.append("Some user stories have no INVEST assessment; review it where this format is appropriate.")
    if isinstance(goal, dict) and not goal.get("out_of_scope"):
        warnings.append("OUT of scope is empty; confirm whether relevant exclusions need to be stated.")
    return warnings


def default_schema_path() -> Path:
    return Path(__file__).resolve().parent.parent / "templates" / "prd-schema.json"


def validate_file(path: Path, schema_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"file": str(path), "status": "FAIL", "errors": [], "warnings": []}
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        doc = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        result["errors"].append(f"Unable to read input/schema: {exc}")
        return result
    except json.JSONDecodeError as exc:
        result["errors"].append(f"Invalid JSON: {exc}")
        return result
    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        result["errors"].append("Schema must declare JSON Schema Draft 2020-12.")
        return result
    if not isinstance(doc, dict):
        result["errors"].append("PRD root must be a JSON object.")
        return result
    try:
        result["errors"].extend(validate_schema_profile(doc, schema))
    except ValueError as exc:
        result["errors"].append(f"Validator/schema profile error: {exc}")
        return result
    result["errors"].extend(semantic_errors(doc))
    if not result["errors"]:
        result["warnings"].extend(quality_warnings(doc))
    result["status"] = "PASS" if not result["errors"] else "FAIL"
    return result


def self_test(schema_path: Path) -> int:
    base = {
        "schema_version": "1.0", "status": "draft", "mode": "fast", "domain": "general",
        "goal": {"purpose": "Clarify the task", "in_scope": ["clarification"], "out_of_scope": []},
        "requirements": {"functional": [], "non_functional": []},
        "acceptance": [{
            "id": "ACC-1", "statement": "The user can verify the requested outcome",
            "verification_method": "manual_review", "expected_result": "A visible review checklist is complete",
            "kind": "human_acceptance", "gate": "closure", "required": True
        }],
        "open_questions": [{
            "id": "Q-1", "question": "What is the preferred deadline?",
            "blocking": False, "owner": "user", "status": "open"
        }]
    }
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    cases = []
    def case(name: str, doc: dict[str, Any], expected: str) -> None:
        errors = validate_schema_profile(doc, schema) + semantic_errors(doc)
        actual = "PASS" if not errors else "FAIL"
        cases.append((name, expected, actual, errors))
    case("draft-may-retain-open-question", base, "PASS")
    ready = json.loads(json.dumps(base))
    ready["status"] = "ready_for_plan"
    case("ready-requires-user-consensus", ready, "FAIL")

    ready_confirmed = json.loads(json.dumps(base))
    ready_confirmed["status"] = "ready_for_plan"
    ready_confirmed["user_confirmation"] = {"consensus_confirmed": True}
    case("ready-with-consensus-and-no-blocker", ready_confirmed, "PASS")

    confirmed_with_blocker = json.loads(json.dumps(base))
    confirmed_with_blocker["status"] = "ready_for_plan"
    confirmed_with_blocker["user_confirmation"] = {"consensus_confirmed": True}
    confirmed_with_blocker["open_questions"][0]["blocking"] = True
    case("ready-rejects-open-blocker", confirmed_with_blocker, "FAIL")

    duplicate = json.loads(json.dumps(base))
    duplicate["acceptance"].append(dict(duplicate["acceptance"][0]))
    case("duplicate-acceptance-id", duplicate, "FAIL")

    wrong_gate = json.loads(json.dumps(base))
    wrong_gate["acceptance"][0]["gate"] = "verification"
    case("human-acceptance-requires-closure", wrong_gate, "FAIL")

    bad_adr = json.loads(json.dumps(base))
    bad_adr["adrs"] = [{"id":"ADR-1","title":"Choice","context":"Context","decision":"Selected","alternatives":["A"],"status":"accepted"}]
    case("accepted-adr-needs-two-options", bad_adr, "FAIL")

    unknown_property = json.loads(json.dumps(base))
    unknown_property["unexpected_control_state"] = "closed"
    case("unknown-root-property-rejected", unknown_property, "FAIL")

    no_acceptance = json.loads(json.dumps(base))
    no_acceptance["acceptance"] = []
    case("acceptance-list-cannot-be-empty", no_acceptance, "FAIL")

    malformed_collection = json.loads(json.dumps(base))
    malformed_collection["facts"] = None
    case("malformed-input-never-crashes", malformed_collection, "FAIL")

    ok = True
    for name, expected, actual, errors in cases:
        passed = expected == actual
        ok = ok and passed
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: expected={expected}, actual={actual}")
        for error in errors:
            print(f"  - {error}")
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'} ({len(cases)} cases)")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a structured grill-to-PRD JSON artifact.")
    parser.add_argument("paths", nargs="*", help="PRD JSON files")
    parser.add_argument("--schema", type=Path, default=default_schema_path(), help="Draft 2020-12 schema")
    parser.add_argument("--json", action="store_true", help="Machine-readable result")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic self-tests")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test(args.schema)
    if not args.paths:
        parser.error("provide at least one PRD JSON file or --self-test")
    results = [validate_file(Path(p), args.schema) for p in args.paths]
    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"[{r['status']}] {r['file']}")
            for error in r["errors"]:
                print(f"  FAIL: {error}")
            for warning in r["warnings"]:
                print(f"  WARN: {warning}")
        print(f"== prd_validate: {'FAIL' if any(r['status'] == 'FAIL' for r in results) else 'PASS'} ==")
    return 1 if any(r["status"] == "FAIL" for r in results) else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
