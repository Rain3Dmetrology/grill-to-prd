#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graph_derive.py — 从 prd.json 派生 flat/graph 两种视图（零依赖，仅标准库）

配套 grill-to-PRD skill。核心思想（Memex 理念）：
  数据保持纯 JSON + Markdown，就完全属于你；不需要图引擎/框架。
  要一个「事实」→ flat list；要发掘「关系」→ graph（边列表）。
  每次启动后运行本脚本，graph 随内容增长，而非重置。

用法:
  python graph_derive.py <prd.json> [--mode flat|graph|both] [--format json|mermaid]
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def flat(doc):
    """事实视图：facts + constraints + gates 的清单。"""
    out = []
    for f in doc.get("facts", []):
        out.append({"id": f.get("id"), "statement": f.get("statement"), "evidence": f.get("evidence", "E0")})
    for c in doc.get("constraints", []):
        out.append({"id": c.get("id"), "statement": c.get("statement"), "evidence": c.get("evidence", "E0")})
    return out


def graph(doc):
    """关系视图：relations 边列表（术语↔抉择↔约束↔验收门）。"""
    return doc.get("relations", [])


def to_mermaid(edges):
    lines = ["graph LR"]
    for e in edges:
        a = e.get("from", "?").replace(" ", "_")
        b = e.get("to", "?").replace(" ", "_")
        t = e.get("type", "link")
        label = {"depends_on": "-->", "constrained_by": "-.->",
                 "locked_by": "==>", "relates": "---"}.get(t, "-->")
        lines.append(f'    {a} {label}|{t}| {b}')
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="grill-to-PRD flat/graph 派生（零依赖）")
    ap.add_argument("prd_json", help="prd-[name].json 路径")
    ap.add_argument("--mode", choices=["flat", "graph", "both"], default="both")
    ap.add_argument("--format", choices=["json", "mermaid"], default="json")
    args = ap.parse_args(argv)
    doc = load(args.prd_json)

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
            print("## flat (facts)")
            for f in result["flat"]:
                print(f'- [{f.get("evidence")}] {f.get("statement")}')
        if "graph" in result:
            print("\n## graph (relations)")
            print(result["graph"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
