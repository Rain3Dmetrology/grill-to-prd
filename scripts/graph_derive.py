#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive flat facts/requirements and an explicit relationship graph from a PRD JSON.

The script does not discover hidden relations. It only renders information
already present in the PRD artifact.
"""
import argparse
import json
import sys


def flat(doc):
    """Create a readable inventory from the current PRD schema, plus legacy inputs."""
    out = []

    def add_items(key, category, fields):
        values = doc.get(key, [])
        if not isinstance(values, list):
            return
        for item in values:
            if not isinstance(item, dict):
                continue
            row = {"id": item.get("id"), "category": category}
            for field in fields:
                if field in item:
                    row[field] = item[field]
            out.append(row)

    goal = doc.get("goal", {})
    if isinstance(goal, dict):
        for item in goal.get("success_criteria", []) if isinstance(goal.get("success_criteria", []), list) else []:
            if isinstance(item, dict):
                out.append({"id": item.get("id"), "category": "success_criterion",
                            "statement": item.get("statement"), "method": item.get("method")})

    add_items("facts", "fact", ["statement", "status", "source", "limitations"])
    requirements = doc.get("requirements", {})
    if isinstance(requirements, dict):
        for key, category in (("functional", "functional_requirement"), ("non_functional", "non_functional_requirement")):
            for item in requirements.get(key, []) if isinstance(requirements.get(key, []), list) else []:
                if isinstance(item, dict):
                    out.append({"id": item.get("id"), "category": category,
                                "statement": item.get("statement"), "priority": item.get("priority")})
    add_items("acceptance", "acceptance", ["statement", "verification_method", "expected_result", "kind", "gate", "required"])
    add_items("assumptions", "assumption", ["statement", "status", "impact", "validation_method"])
    add_items("decisions", "decision", ["question", "chosen_option", "status", "decision_owner"])
    add_items("open_questions", "open_question", ["question", "blocking", "owner", "status"])

    # Backward-compatible read support for v0.3.x artifacts.
    add_items("constraints", "legacy_constraint", ["statement", "evidence"])
    add_items("gates", "legacy_gate", ["definition", "acceptance_command", "evidence_level", "status"])
    return out


def graph(doc):
    """Return explicitly authored relations only."""
    edges = doc.get("relations", [])
    return edges if isinstance(edges, list) else []


def to_mermaid(edges):
    lines = ["graph LR"]
    operators = {
        "depends_on": "-->",
        "constrained_by": "-.->",
        "locked_by": "==>",
        "relates": "---",
        "supports": "==>",
        "contradicts": "-.->",
    }
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("from", "?")).replace(" ", "_")
        target = str(edge.get("to", "?")).replace(" ", "_")
        relation = str(edge.get("type", "relates"))
        lines.append(f"    {source} {operators.get(relation, '-->')}|{relation}| {target}")
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Derive PRD flat/graph views (stdlib only).")
    parser.add_argument("prd_json", help="Path to prd-[name].json")
    parser.add_argument("--mode", choices=["flat", "graph", "both"], default="both")
    parser.add_argument("--format", choices=["json", "mermaid"], default="json")
    args = parser.parse_args(argv)

    with open(args.prd_json, encoding="utf-8") as stream:
        doc = json.load(stream)
    result = {}
    if args.mode in ("flat", "both"):
        result["flat"] = flat(doc)
    if args.mode in ("graph", "both"):
        edges = graph(doc)
        result["graph"] = to_mermaid(edges) if args.format == "mermaid" else edges

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "flat" in result:
            print("## flat (requirements and facts)")
            for item in result["flat"]:
                print(f"- [{item.get('category')}] {item.get('id')}: {item.get('statement') or item.get('question') or ''}")
        if "graph" in result:
            print("\n## graph (explicit relations)")
            print(result["graph"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
