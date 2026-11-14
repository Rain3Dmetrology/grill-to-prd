# grill-to-PRD — 通用需求引导翻译官 / Universal Requirement Elicitation Translator

[English](#english) | [中文](#中文)

---

## English

Translate vague intent into structured PRDs. The core is not "writing docs" — it is **nailing down assumptions, acceptance gates, boundaries and priorities before any work starts**. Runs as a requirements-intake Skill; execution authority comes from Harness LOOP Specification v3.1.1.

**Domain-agnostic**: software development, product planning, market/business, tech/model selection, daily life — also serves as the requirement entry for expert teams.

### Quick Start (trigger examples)

| Scenario | One-liner |
|---|---|
| Tech selection | "Use grill-to-PRD to sort out my requirements & acceptance criteria for choosing [X]" |
| Market research | "Use grill-to-PRD to clarify the scope and acceptance gates of [research topic]" |
| Life decision | "Use grill-to-PRD to plan [task]: goal, boundary, what counts as success" |

Routing: complex → **Deep mode** (multi-round grilling → frontier-empty proof → PRD); simple → **Fast mode** (3-5 lettered options → slim PRD); oversized task → **wayfinder planning** first. Output defaults to `prd-*.md`; emit `prd-*.json` only when structured downstream consumption requires it.

### Three-Stage Architecture (aligned with mattpocock/skills)

```
wayfinder (planner)   oversized fuzzy task → decision-ticket map → solve ticket by ticket
grilling (interviewer) multi-round frontier design tree: full frontier + recommended answers; stops only when frontier is empty
to-spec (synthesizer) one-shot synthesis (no interviewing) → PRD with LONG stories + execution/verification decisions + acceptance mount points
grill-to-PRD = unified entry + governance glue (B1-B7 ledger / G1-G3 gates / E0-E3 evidence grading / dual-form output)
```

### Modes + Domain Adapters

| Mode | For | Kernel |
|---|---|---|
| **Deep mode** | high-stakes/multi-decision/irreversible choices | grilling design tree + round gate (frontier-empty proof) + user-consensus gate + ADR/glossary trail |
| **Fast mode** | quick scope+acceptance freeze, minimal interaction | Lettered Options ("1A,2C,3B" batch) + MoSCoW light priority |
| **wayfinder** | task exceeds one session | destination → frontier mapping → decision-ticket map → per-ticket solving |
| **Domain adapters** | fact-dense domains | `references/domain-adapters.md` injects adapters (**6 built-in**: codebase / HF models / market / patent / business-model / daily-life) |

> Deep/Fast grade the **interview intensity**, not the domain; domain differences go through adapters.

### Key Capabilities (v0.3.2)

- **Programmatic PRD validation gate (v0.3.2)**: `scripts/prd_validate.py` (zero-dependency) — Draft 2020-12 PRD structure plus semantic checks; structural/semantic FAIL always blocks, while quality notices remain WARN and cannot be masked by a numeric score. The validator does not grant vendor or tool permissions
- **Agent-facing triple modules (v0.3.2)**: `prd-schema.json` adds `data_objects` (entity dictionary + state machine) / `pipeline_constraints` (pipeline topology) / `error_personality` (exception fallback personality) — lets downstream research/architecture agents unambiguously consume requirement structure, priority and pipeline constraints (opt-in)
- **Layered embedded governance (v0.3.1)**: stable core verbatim / frequently-evolving clauses summarized / stage-specific rules delegated downstream
- **Three Hard Rules on question quality**: No Vague Metrics / Problem Before Solution / INVEST Stories
- **Priority frameworks**: MoSCoW / RICE / ICE / Kano + Hybrid combo; per-US priority + trade-off adjudication table
- **PRD structure**: 11 sections (prd-master aligned) + BDD Given-When-Then / Checklist dual acceptance format
- **Decision trail**: ADR requires ≥2 alternatives (Alternatives Required) + requirements traceability matrix REQ→Design→Impl→Tests
- **Acceptance mount points** (seams generalized): code=test seam / market=cross-validated data sources / life=key checkpoints
- **Guards & linting**: vibeguard three-layer guards + learn loop + `truncation_lint.py` truncation lint

### Output

- Dual form: `prd-[name].md` (narrative) + `prd-[name].json` (structured, schema in `templates/prd-schema.json`)
- Layered: flat list (facts) / graph (relations via zero-dependency `scripts/graph_derive.py`)
- Ledger: `ledger.md` + `ledger.json`
- Downstream: dev scenarios can continue with to-tickets; research scenarios feed expert-team parameter cards

### Install

```powershell
# One-click install into WorkBuddy skill dir (~/.workbuddy/skills/grill-to-prd)
powershell -ExecutionPolicy Bypass -File .\install.ps1
# Custom target:
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "<your-skills-dir>"
```

Atomic replace (temp dir + atomic rename + rollback). Version-drift printout on every install; re-run install.ps1 after upgrades. Or copy the folder manually — scripts use relative paths (platform-neutral).

### Governance Boundary

The execution authority is Harness LOOP Specification v3.1.1. Update the pinned reference and field mapping when the normative spec changes; do not duplicate its control text in this Skill. Version bump without L-review or user confirmation is forbidden.

### License

MIT. Third-party attribution in `NOTICE.md`. The validator uses Python's standard library and a documented subset of JSON Schema Draft 2020-12 keywords.

---

## 中文

把模糊意图翻译成结构化 PRD。核心不是写文档，而是**动手前把话说透、把假设暴露、把验收门钉死、把边界收敛、把优先级排清**。执行治理以《Harness LOOP Specification v3.1.1》为准；本 Skill 仅负责需求入口。

**通用定位**：**域无关**的需求引导引擎——软件开发、产品规划、市场商业、技术/模型选型、日常生活任意场景，也可作为专家/专家团的需求入口。

### 30 秒上手（触发示例）

| 场景 | 一句话触发 |
|---|---|
| 技术选型 | "用 grill-to-PRD 梳理一下我选 [X] 方案的需求与验收标准" |
| 市场调研 | "帮我用 grill-to-PRD 把 [调研主题] 的需求边界和验收门理清楚" |
| 生活决策 | "用 grill-to-PRD 帮我规划 [事项]，要目标、边界、怎么算成功" |

触发后自动路由：复杂任务走**深度模式**（多轮追问 → frontier 空证明 → PRD），简单任务走**快速模式**（3-5 问字母选项 → 精简 PRD），超长任务先走 **wayfinder 规划**。默认产出 `prd-*.md`；仅在下游需要结构化消费时生成 `prd-*.json`。

### 三段式架构（对齐 mattpocock/skills）

```
wayfinder（规划器 · 域无关）  大型模糊任务 → 决策票据地图 → 逐票据解决（超长任务入口）
grilling（追问器 · 域无关）   多轮 frontier 设计树：整前沿+推荐答案+重算，frontier 空才停
to-spec（合成器 · 域无关）    单次合成（不追问）→ PRD：LONG stories + 执行/验证决策 + 验收挂载点
grill-to-PRD = 统一入口 + 治理胶水（B1-B7 台账 / G1-G3 验收门 / E0-E3 证据分级 / 双形态输出）
```

### 双模式 + 领域适配层

| 模式 | 场景 | 内核 |
|---|---|---|
| **深度模式** | 深度/高风险/多决策/需沉淀不可逆抉择 | grilling 多轮设计树 + **轮次门禁（frontier 空证明）+ 用户共识确认门** + 决策留痕（ADR + 术语表） |
| **快速模式** | 快速固化需求边界+验收标准、最小交互 | Lettered Options（1A,2C,3B 批量）+ MoSCoW 轻量优先级 |
| **wayfinder 规划** | 任务超一个会话 | 目的地→测绘前沿→决策票据地图→逐票据解决（本地 markdown tracker 轻量落地） |
| **领域适配层** | 特定领域事实密集 | `references/domain-adapters.md` 注入适配器（**6 个内置**：代码库/HF 模型/市场/专利/商业模式/日常生活） |

> 深度/快速是**追问强度分级**，与领域无关；领域差异一律走适配层。

### 核心能力（v0.3.2）

- **程序化 PRD 校验门禁（v0.3.2）**：`scripts/prd_validate.py`（零依赖）——Draft 2020-12 结构与语义检查；结构性/语义 FAIL 必须阻断，质量建议仅为 WARN，不能用评分掩盖硬失败。校验器不授予供应商或工具权限
- **面向 Agent 三模块（v0.3.2）**：`prd-schema.json` 增 `data_objects`（实体数据字典+状态机）/ `pipeline_constraints`（Pipeline 拓扑约束）/ `error_personality`（异常降级人格）——供下游调研/架构 Agent 无歧义消费需求结构关系、优先级与 pipeline 约束（按需追加）
- **分层内嵌治理（v0.3.1）**：稳定内核逐字内嵌 / 高频演进条款摘要 / 阶段专属机制由下游承担（防范围蔓延）
- **追问质量三 Hard Rules**：No Vague Metrics（可量化）/ Problem Before Solution（先问题后方案）/ INVEST Stories
- **优先级框架**：MoSCoW / RICE / ICE / Kano + Hybrid 组合法；per-US 优先级 + 取舍裁决表
- **PRD 结构**：11 节（对齐 prd-master）+ BDD Given-When-Then/Checklist 验收双格式
- **决策留痕**：ADR 强制 ≥2 备选方案 + 需求追踪矩阵 REQ→Design→Impl→Tests
- **验收挂载点**（seams 推广）：代码=测试缝隙 / 市场=数据源交叉验证点 / 生活=关键检查点
- **守卫与机检**：vibeguard 三层守卫 + learn 闭环 + `truncation_lint.py` 截断机检

### 输出

- 双形态：`prd-[name].md`（叙事）+ `prd-[name].json`（结构，schema 见 `templates/prd-schema.json`）
- 分层：flat list（事实）/ graph（关系，`scripts/graph_derive.py` 零依赖派生）
- 台账：`ledger.md` + `ledger.json`
- 下游：开发场景可续 to-tickets；调研场景作为专家团任务卡/参数卡输入

### 安装

```powershell
# 一键安装到 WorkBuddy 技能目录（~/.workbuddy/skills/grill-to-prd）
powershell -ExecutionPolicy Bypass -File .\install.ps1
# 自定义目标：
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "<你的技能目录>"
```

原子替换（临时目录 + 原子改名 + 失败回滚）。每次安装打印版本漂移提示；升级后重跑 install.ps1 即同步。也可手动复制目录——脚本相对路径调用，平台无关。

### 治理边界

执行权威为 Harness LOOP Specification v3.1.1。规范升级时更新固定版本引用与字段映射；不得在本 Skill 中重复维护规范控制正文。未经 L 复盘或用户确认不 bump 版本。

### 许可证

MIT，第三方 attribution 见 `NOTICE.md`。校验器仅使用 Python 标准库，支持仓库明确列出的 JSON Schema Draft 2020-12 关键字子集。
