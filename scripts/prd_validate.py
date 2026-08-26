#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd_validate.py — 程序化 PRD 校验门禁（Google 方案一「阶段三」自建平台无关版）

配套 grill-to-PRD skill（v0.3.2+）。零依赖（仅标准库）、离线安全、平台无关。
四维检查 + 0-100 评分 + 修复指令（"错误信息=修复指令"原则）。

四维（对齐 Google 方案一阶段三，各 25 分）：
  1. 目标可量化性  measurable_goals   —— 是否有数字/百分比断言、success metrics
  2. 边界清晰度    boundary_clarity    —— 是否 ≥3 项显式 Non-Goals/Out of Scope
  3. 测试缝隙      test_seams          —— 是否显式定义验证缝隙与验收命令
  4. 技术合规性    tech_compliance     —— 是否引用未经许可的第三方服务（受信任域名白名单）

输入：prd-*.json（结构层，首选，逐字段断言）或 prd-*.md（叙事层，启发式）。
评分 ≥ --threshold（默认 80）判 PASS；否则 FAIL 并给出逐条修复指令。
退出码 0=PASS / 1=FAIL / 2=用法错误，可作 CI 门禁。脚本缺失或环境无 Python 时跳过，不阻断主管线。

用法:
  python prd_validate.py <prd-*.json|prd-*.md>... [--threshold N] [--json] [--quiet]
  python prd_validate.py --self-test
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

# 受信任域名白名单（技术合规性维：引用了白名单外的外部服务即 WARN 扣分）
# 语义：仅列「开发基础设施 + 信息检索」默认许可（代码托管/模型库/论文/百科/包索引/搜索引擎）；
# 业务级第三方（云厂商/模型 API/SaaS/支付等）须显式写入 PRD 的 trusted_domains 或视为需许可。
# 扩展方式：按领域在 skill 的 references/domain-adapters.md 维护，此处为通用默认集。
TRUSTED_DOMAINS_DEFAULT = {
    # 开发基础设施
    "github.com", "huggingface.co", "arxiv.org", "wikipedia.org",
    "pypi.org", "npmjs.com", "crates.io",
    # 信息检索（日常事实取证，非服务依赖）
    "google.com", "bing.com", "baidu.com",
}

# ---- 可量化指标识别：数字/百分比/时间/规模单位 ----
QUANT_PATTERNS = [
    re.compile(r"\d+(?:\.\d+)?\s*%"),                          # 百分比
    re.compile(r"\d+(?:\.\d+)?\s*(?:ms|s|sec|min|h|day|GB|MB|KB|TB|TPS|QPS|RPS|Mbps)\b", re.I),  # 英文单位
    re.compile(r"\d+(?:\.\d+)?\s*(?:毫秒|微秒|秒|分钟|小时)"),   # 中文时间单位（歧义低，避免 天/周/月/年 与日期混淆）
    re.compile(r"\d+(?:\.\d+)?\s*(?:倍|x|X|万|亿|千)"),          # 倍数/中文量级
    re.compile(r"(?:P95|P99|MTTR|MTBF|NPS|SLA|DAU|MAU|CTR|CVR|ROI|TPS)\b", re.I),  # 指标词
    re.compile(r"(?:≤|≥|<=|>=|>|<)\s*\d+(?:\.\d+)?"),           # 阈值比较
]
VAGUE_METRIC = re.compile(
    r"(?:尽快|尽量|足够快|性能好|体验好|好用|流畅|稳定可靠|快一些|多一些|更快|更好|更高)",
    re.I,
)
# 空验收命令（"工作正常"式废话）
VAGUE_ACCEPTANCE = re.compile(
    r"(?:工作正常|正常运行|能跑|通过测试|验收通过|无异常|符合预期|ok|done|works)\s*$",
    re.I,
)
# 未经许可的第三方服务引用（技术合规性）：识别 "调用/接入/使用 X 服务" 但 X 不在白名单
THIRD_PARTY_CALL = re.compile(
    r"(?:调用|接入|使用|依赖|集成|部署到|采用)\s*([A-Za-z0-9][A-Za-z0-9.-]+\.(?:com|cn|io|ai|net|org|cloud|dev))",
    re.I,
)

PLACEHOLDER = re.compile(r"(?:TODO|TBD|FIXME|XXX|待定|待补|待填|TBC|\.\.\.)", re.I)


def _safe(data, *keys, default=None):
    """逐层安全取值，任何类型错误返回 default。"""
    cur = data
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
        if cur is None:
            return default
    return cur


def _has_quantifiable(text):
    if not text:
        return False
    return any(rx.search(text) for rx in QUANT_PATTERNS)


def check_json(data, strict=False):
    """对 prd-*.json 结构层逐字段断言。扣分制，四维各 25 分，返回 (score, findings)。

    strict=True 时，第三方服务引用判 HARD-FAIL 硬门禁；默认（strict=False）判 WARN 扣分。
    """
    findings = []  # (dim, rule, severity, message, fix)

    goal = _safe(data, "goal", default={}) or {}
    purpose = goal.get("purpose", "") if isinstance(goal, dict) else ""
    purpose = purpose or ""  # 防御 None（键存在但值为 null 时）
    us = _safe(data, "user_stories", default=[]) or []
    us = us if isinstance(us, list) else []
    gates = _safe(data, "gates", default=[]) or []
    gates = gates if isinstance(gates, list) else []
    oos = _safe(data, "goal", "out_of_scope", default=[]) or []
    oos = oos if isinstance(oos, list) else []
    in_scope = _safe(data, "goal", "in_scope", default=[]) or []
    in_scope = in_scope if isinstance(in_scope, list) else []
    tds = _safe(data, "trusted_domains", default=[]) or []
    tds = tds if isinstance(tds, list) else []

    # 维度1：目标可量化性 /25（扣分制）
    m_score = 25
    if not purpose or PLACEHOLDER.search(purpose):
        m_score -= 5
        findings.append(("measurable_goals", "goal.purpose", "FAIL",
                         "主目标 purpose 缺失或为占位符",
                         "补写：PRD 头部「目的（用户原话）」冻结的、非占位的主目标。"))
    if not us:
        m_score -= 5
        findings.append(("measurable_goals", "user_stories", "FAIL",
                         "user_stories 为空", "补写：至少 1 条 user story（INVEST 合规）。"))

    # 可量化指标：扫描整个 PRD 文本（goal/constraints/facts/user_stories 等全字段），避免漏检
    metrics_text = json.dumps(data, ensure_ascii=False)
    if _has_quantifiable(metrics_text):
        if VAGUE_METRIC.search(metrics_text):
            m_score -= 3
            findings.append(("measurable_goals", "vague-metric", "WARN",
                             "含模糊指标词（尽快/尽量/足够快等）",
                             "把模糊指标改写为可量化目标（Hard Rule 1: No Vague Metrics）。"))
    else:
        m_score -= 10
        findings.append(("measurable_goals", "quantifiable", "FAIL",
                         "未发现可量化指标（数字/百分比/阈值/指标词）",
                         "补写：把模糊指标改可量化，如「加载快」→「P95 < 2s on 4G」；「可靠」→「99.9% 可用，MTTR<1h」。"))

    # 维度2：边界清晰度 /25（扣分制）
    b_score = 25
    if len(oos) < 3:
        b_score -= 15
        findings.append(("boundary_clarity", "out_of_scope", "FAIL",
                         f"Out of Scope 仅 {len(oos)} 项（需 ≥3）",
                         "补写：显式列出 ≥3 项 Non-Goals/Out of Scope（含已否决的选项）。"))
    if not in_scope:
        b_score -= 10
        findings.append(("boundary_clarity", "in_scope", "FAIL",
                         "IN scope 为空", "补写：明确 IN scope 边界（范围收敛清单第 1 项）。"))

    # 维度3：测试缝隙 /25（扣分制）
    t_score = 25
    if len(gates) < 3:
        t_score -= 10
        findings.append(("test_seams", "gates", "FAIL",
                         f"验收门仅 {len(gates)} 个（需 G1/G2/G3）",
                         "补写：定义 G1 单元 / G2 集成 / G3 实机 三层验收门（验收命令先行 B2）。"))
    missing_cmd = 0
    missing_mount = False
    for g in gates:
        if not isinstance(g, dict):
            continue
        cmd = g.get("acceptance_command", "")
        if not cmd or VAGUE_ACCEPTANCE.search(str(cmd)) or PLACEHOLDER.search(str(cmd)):
            missing_cmd += 1
        if not g.get("mount_point"):
            missing_mount = True
    if missing_cmd:
        t_score -= min(15, 5 * missing_cmd)
        findings.append(("test_seams", "acceptance_command", "FAIL",
                         f"{missing_cmd} 个验收门缺可执行验收命令（或为空话）",
                         "补写：每门附一条可执行验收命令（可验证，非「工作正常」）。"))
    if missing_mount:
        t_score -= 5
        findings.append(("test_seams", "mount_point", "WARN",
                         "部分验收门缺 mount_point（验收挂载点）",
                         "补写：每门验收命令挂载到明确挂载点（代码=seam/市场=数据源交叉点/生活=检查点）。"))

    # 维度4：技术合规性 /25（扣分制）
    c_score = 25
    if not tds:
        c_score -= 5
        findings.append(("tech_compliance", "trusted_domains", "WARN",
                         "trusted_domains（受信任域名白名单）为空",
                         "补写：声明本 PRD 事实取证允许的受信任域名，白名单外结论最高 INFERRED。"))
    full_text = json.dumps(data, ensure_ascii=False)
    allowed = TRUSTED_DOMAINS_DEFAULT | set(tds)
    for m in THIRD_PARTY_CALL.finditer(full_text):
        domain = m.group(1).lower()
        if domain not in allowed and not any(
                domain.endswith("." + d) or d.endswith("." + domain) for d in allowed):
            c_score -= 12
            sev = "HARD-FAIL" if strict else "WARN"
            findings.append(("tech_compliance", "third-party", sev,
                             f"引用了未许可第三方服务：{domain}",
                             "修复：① 若确需该服务，加入 trusted_domains 白名单并注明许可；② 否则替换为系统指定平台组件。"))

    score = max(0, m_score) + max(0, b_score) + max(0, t_score) + max(0, c_score)
    return score, findings


def check_md(text, strict=False):
    """对 prd-*.md 叙事层做启发式检查（置信低于 JSON）。四维各 25 分，与 json 口径对齐。"""
    findings = []
    m_score = 25
    b_score = 25
    t_score = 25
    c_score = 25
    # 目标可量化性
    if not _has_quantifiable(text):
        m_score -= 15
        findings.append(("measurable_goals", "quantifiable", "FAIL",
                         "未发现可量化指标", "补写可量化 success metrics（数字/百分比/阈值）。"))
    # 边界清晰度：Out of Scope 章节
    oos = re.search(r"(?:Out of Scope|非目标|不做什么|OUT of scope)", text, re.I)
    if not oos:
        b_score -= 15
        findings.append(("boundary_clarity", "out_of_scope", "FAIL",
                         "未见 Out of Scope / 非目标章节", "补写 ≥3 项 Non-Goals。"))
    # 测试缝隙：验收门/验收命令
    gates = re.search(r"(?:验收门|Acceptance|G1|G2|G3)", text, re.I)
    if not gates:
        t_score -= 15
        findings.append(("test_seams", "gates", "FAIL",
                         "未见验收门/验收命令章节", "补写 G1/G2/G3 验收门 + 验收命令。"))
    # 技术合规性：第三方服务引用（默认 WARN 扣分，strict 时硬门禁，与 json 对齐）
    for m in THIRD_PARTY_CALL.finditer(text):
        domain = m.group(1).lower()
        if domain not in TRUSTED_DOMAINS_DEFAULT and not any(
                domain.endswith("." + d) or d.endswith("." + domain) for d in TRUSTED_DOMAINS_DEFAULT):
            c_score -= 12
            sev = "HARD-FAIL" if strict else "WARN"
            findings.append(("tech_compliance", "third-party", sev,
                             f"引用了未许可第三方服务：{domain}",
                             "修复：① 若确需该服务，声明 trusted_domains 白名单；② 否则替换为平台组件。"))
    # 占位符
    if PLACEHOLDER.search(text):
        m_score -= 5
        findings.append(("structural", "placeholder", "WARN",
                         "含 TODO/TBD/待定 等占位符", "清除占位符或在 open_questions 显式列出。"))
    score = max(0, m_score) + max(0, b_score) + max(0, t_score) + max(0, c_score)
    return score, findings


def validate_path(path, threshold, strict=False):
    p = Path(path)
    try:
        if p.suffix.lower() == ".json":
            data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            score, findings = check_json(data, strict)
            mode = "json"
        else:
            text = p.read_text(encoding="utf-8", errors="replace")
            score, findings = check_md(text, strict)
            mode = "md"
    except OSError as e:
        return {"file": str(p), "mode": "?", "score": 0, "threshold": threshold,
                "verdict": "FAIL", "findings": [("structural", "read", "FAIL", "unreadable", str(e))]}
    except json.JSONDecodeError as e:
        return {"file": str(p), "mode": "json", "score": 0, "threshold": threshold,
                "verdict": "FAIL", "findings": [("structural", "json", "FAIL", "invalid-json", str(e))]}
    verdict = "PASS" if (score >= threshold and not any(
        f[2] == "HARD-FAIL" for f in findings)) else "FAIL"
    return {"file": str(p), "mode": mode, "score": score, "threshold": threshold,
            "verdict": verdict, "findings": findings}


def self_test():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        good = {
            "goal": {"purpose": "把模糊需求收敛为结构化 PRD",
                     "in_scope": ["需求引导", "验收定义"],
                     "out_of_scope": ["编码实现", "部署运维", "UI 设计"]},
            "gates": [
                {"id": "G1", "definition": "单元", "acceptance_command": "python prd_validate.py prd.json --threshold 80", "mount_point": "prd.json"},
                {"id": "G2", "definition": "集成", "acceptance_command": "下游 agent 识别准确率≥90%", "mount_point": "识别测试"},
                {"id": "G3", "definition": "实机", "acceptance_command": "用户确认 P95<2s", "mount_point": "实测"},
            ],
            "trusted_domains": ["github.com", "huggingface.co"],
            "user_stories": [
                {"id": "US-001", "title": "量化", "so_that": "P95 < 2s on 4G",
                 "acceptance_criteria": ["Given 4G / When 加载 / Then P95<2000ms"]}
            ],
        }
        bad = {"goal": {"purpose": "TODO", "out_of_scope": ["x"]}, "gates": [], "user_stories": []}
        third = {"goal": {"purpose": "ok", "in_scope": ["a"], "out_of_scope": ["a", "b", "c"]},
                 "gates": [{"id": "G1", "acceptance_command": "python t.py", "mount_point": "x"},
                           {"id": "G2", "acceptance_command": "python t2.py", "mount_point": "x"},
                           {"id": "G3", "acceptance_command": "python t3.py", "mount_point": "x"}],
                 "trusted_domains": ["github.com"],
                 "user_stories": [{"id": "US-001", "so_that": "P95<2s", "acceptance_criteria": ["x"]}],
                 "constraints": [{"id": "C1", "statement": "调用 evil-third-party.com 服务", "evidence": "E1"}]}
        cases = [
            ("good-pass", good, 80, False, "PASS"),
            ("bad-fail", bad, 80, False, "FAIL"),
            ("third-party-warn-pass", third, 80, False, "PASS"),   # 默认 WARN 不硬门禁
            ("third-party-strict-fail", third, 80, True, "FAIL"),  # --compliance-strict 硬门禁
        ]
        for name, data, thr, strict, expect in cases:
            fp = root / f"{name}.json"
            fp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            r = validate_path(fp, thr, strict)
            got = r["verdict"]
            good = got == expect
            ok = ok and good
            print(f"  [{'ok' if good else 'MISMATCH'}] {name}: expect={expect} got={got} score={r['score']}")
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="程序化 PRD 校验门禁（四维 0-100 评分 + 修复指令，零依赖）")
    ap.add_argument("paths", nargs="*", help="prd-*.json 或 prd-*.md 文件")
    ap.add_argument("--threshold", type=int, default=80, help="流转阈值（默认 80，对齐 Google 方案一）")
    ap.add_argument("--compliance-strict", action="store_true",
                    help="技术合规性第三方服务引用升级为 HARD-FAIL 硬门禁（默认 WARN 扣分）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--quiet", action="store_true", help="只输出结论行")
    ap.add_argument("--self-test", action="store_true", help="临时目录注入自测，不污染工作区")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.paths:
        ap.print_usage(sys.stderr)
        return 2
    results = [validate_path(p, args.threshold, args.compliance_strict) for p in args.paths]
    any_fail = any(r["verdict"] == "FAIL" for r in results)
    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"[{r['verdict']}] {r['file']} (mode={r['mode']}) score={r['score']}/{r['threshold']}")
            if not args.quiet:
                for dim, rule, sev, msg, fix in r["findings"]:
                    print(f"  {sev} [{dim}] {rule}: {msg}")
                    print(f"      → 修复: {fix}")
        print(f"== prd_validate: {'FAIL' if any_fail else 'PASS'} | files={len(results)} ==")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
