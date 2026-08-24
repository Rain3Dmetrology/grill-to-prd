#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""truncation_lint.py — R13 截断标记机检（配套《人机协作 Loop 治理规范》v2.3 §六.8）

零依赖（仅标准库）、离线安全。FAIL=已知截断标记/未闭合代码围栏/--min-lines 不达标；
WARN=末行悬置（--strict 时升级 FAIL）。退出码 0=PASS / 1=FAIL / 2=用法错误，可作 CI 门禁。
脚本缺失或环境无 Python 时跳过，不阻断主管线。

用法:
  python truncation_lint.py <文件|目录>... [--min-lines N] [--strict] [--json] [--quiet]
  python truncation_lint.py --self-test
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

MARKERS = [
    (re.compile(r"\[\s*omitted[^\]]*\]", re.I), "codex-omitted"),
    (re.compile(r"omitted for (?:brevity|length|space)", re.I), "omitted-for-brevity"),
    (re.compile(r"\[\s*\.\.\.?\s*(?:truncated|omitted|remainder)", re.I), "ellipsis-marker"),
    (re.compile(r"output (?:was |has been |is )?truncated", re.I), "output-truncated"),
    (re.compile(r"\[?truncated (?:to fit|at \d+)", re.I), "truncated-tag"),
    (re.compile(r"content truncated", re.I), "content-truncated"),
    (re.compile(r"已截断|被截断|输出截断"), "zh-truncated"),
    (re.compile(r"\[\s*省略\s*\d*\s*行?\s*\]"), "zh-omitted"),
]
FENCE = re.compile(r"^`{3}", re.M)
DANGLERS = ("，", ",", "：", ":", "、", "（", "(", "——", " and", " or")


def scan_file(path, min_lines=0):
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [("WARN", str(path), 0, "unreadable", str(e))]
    lines = text.splitlines()
    findings = []
    for rx, label in MARKERS:
        for m in rx.finditer(text):
            findings.append(("FAIL", str(path), text.count("\n", 0, m.start()) + 1, label, m.group(0)[:60]))
    fences = list(FENCE.finditer(text))
    if len(fences) % 2:
        last = fences[-1]
        findings.append(("FAIL", str(path), text.count("\n", 0, last.start()) + 1, "unclosed-fence", f"{len(fences)} fences"))
    tail = next((l.rstrip() for l in reversed(lines) if l.strip()), "")
    if tail.endswith(DANGLERS):
        findings.append(("WARN", str(path), len(lines), "dangling-tail", tail[-40:]))
    if min_lines and len(lines) < min_lines:
        findings.append(("FAIL", str(path), len(lines), "min-lines", f"{len(lines)}<{min_lines}"))
    return findings


def collect(paths):
    files, seen = [], set()
    for p in map(Path, paths):
        if p.is_dir():
            cands = sorted(q for q in p.rglob("*") if q.is_file() and q.suffix.lower() in {".md", ".txt", ".log"})
        elif p.is_file():
            cands = [p]
        else:
            continue
        for c in cands:
            if c not in seen:
                seen.add(c)
                files.append(c)
    return files


def self_test():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "clean.md").write_text("# 标题\n\n正文完整，句号结尾。\n", encoding="utf-8")
        (root / "omitted.md").write_text("# t\n\n前文\n[omitted 12000 chars]\n后文\n", encoding="utf-8")
        (root / "fence.md").write_text("# t\n\n```python\nprint(1)\n", encoding="utf-8")
        (root / "tail.md").write_text("# t\n\n写到一半，\n", encoding="utf-8")
        (root / "short.md").write_text("a\nb\nc\n", encoding="utf-8")
        (root / "zh.md").write_text("检索结果输出截断。\n", encoding="utf-8")
        (root / "en.md").write_text("some text\nOutput truncated by context window\nmore\n", encoding="utf-8")
        cases = [
            ("clean-pass", root / "clean.md", {}, "PASS"),
            ("codex-marker-fail", root / "omitted.md", {}, "FAIL"),
            ("unclosed-fence-fail", root / "fence.md", {}, "FAIL"),
            ("dangling-warn-pass", root / "tail.md", {}, "PASS"),
            ("dangling-strict-fail", root / "tail.md", {"strict": True}, "FAIL"),
            ("min-lines-fail", root / "short.md", {"min_lines": 10}, "FAIL"),
            ("zh-marker-fail", root / "zh.md", {}, "FAIL"),
            ("en-marker-fail", root / "en.md", {}, "FAIL"),
        ]
        for name, path, opts, expect in cases:
            fs = scan_file(path, opts.get("min_lines", 0))
            failed = any(x[0] == "FAIL" for x in fs) or (opts.get("strict") and bool(fs))
            got = "FAIL" if failed else "PASS"
            good = got == expect
            ok = ok and good
            print(f"  [{'ok' if good else 'MISMATCH'}] {name}: expect={expect} got={got}")
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="R13 截断标记机检（零依赖，离线安全）")
    ap.add_argument("paths", nargs="*", help="文件或目录（目录递归扫 .md/.txt/.log）")
    ap.add_argument("--min-lines", type=int, default=0, help="文件最低行数门槛（可证伪的异常短）")
    ap.add_argument("--strict", action="store_true", help="WARN 也计 FAIL")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--quiet", action="store_true", help="只输出结论行")
    ap.add_argument("--self-test", action="store_true", help="临时目录注入自测，不污染工作区")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.paths:
        ap.print_usage(sys.stderr)
        return 2
    files = collect(args.paths)
    findings = []
    for f in files:
        findings.extend(scan_file(f, args.min_lines))
    hard = [x for x in findings if x[0] == "FAIL"]
    soft = [x for x in findings if x[0] == "WARN"]
    fail = bool(hard) or (args.strict and bool(soft))
    verdict = "FAIL" if fail else "PASS"
    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "files": len(files),
            "findings": [
                {"severity": s, "file": f, "line": n, "rule": r, "evidence": e}
                for s, f, n, r, e in findings
            ],
        }, ensure_ascii=False, indent=2))
    elif not args.quiet:
        for s, f, n, r, e in findings:
            print(f"{s} {f}:{n} {r} {e!r}")
        print(f"== truncation_lint: {verdict} | files={len(files)} fail={len(hard)} warn={len(soft)} ==")
    else:
        print(f"== truncation_lint: {verdict} ==")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
