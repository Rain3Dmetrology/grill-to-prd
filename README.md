# grill-to-PRD — 通用需求引导翻译官 / Universal Requirement Elicitation Translator

[English](#english) | [中文](#中文)

## English

Turn ambiguous intent into reviewable requirements. This Skill focuses on **fact-first elicitation, scope clarification, explicit decisions, observable acceptance conditions, and traceable PRD artifacts**. It is a requirements-intake component, not an execution Harness.

### When to use it

| Situation | Trigger example |
|---|---|
| Ambiguous software/product request | "Use grill-to-PRD to clarify the goal, scope and acceptance criteria." |
| Research or technical selection | "Use grill-to-PRD to define the research scope, assumptions and decision criteria." |
| Long multi-session work | "Use wayfinder to map the destination and decision tickets first." |

### Workflow

```
User intent
   └─ Fast / Deep elicitation
          ├─ inspect facts before asking
          ├─ separate facts, assumptions and user decisions
          ├─ track blocking and non-blocking unknowns
          └─ draft PRD / confirm requirements consensus
                    └─ downstream Harness + domain workflows
```

- **Fast**: ask only questions that materially change goal, scope, success criteria or a key decision. Zero questions can be correct when the request is already clear.
- **Deep**: use a decision tree and recompute the current question frontier after each user response.
- **Wayfinder**: use only for work spanning sessions or containing substantial dependencies; reuse an existing issue tracker instead of creating a duplicate.
- A **Draft PRD** may retain explicit unknowns. **Ready for plan** requires no open blocking questions and explicit user confirmation of shared understanding.

### Authority boundary

The normative execution authority is [Harness LOOP Specification v3.1.1](https://github.com/Rain3Dmetrology/agent-harness-loop-spec/blob/84e74b98e628a9358765a261e281fb474018a686/SPEC.zh-CN.md). This Skill is Guidance only. It does not implement TaskContract lifecycle, budgets, permissions, effect approvals, Effect Journal, leases, evidence validity, recovery or final closure.

Requirements consensus is not plan approval or execution authorization. A PRD is an artifact, not a TaskContract or execution-state SSOT. See `references/harness-interop.md` for field mapping.

### Outputs

- **Default**: `prd-[name].md` for human review.
- **Optional**: `prd-[name].json` when a downstream Agent or program needs structured data.
- **Optional modules**: user stories, ADRs, traceability matrix, `data_objects`, `pipeline_constraints`, `error_personality`, and graph views are included only when they reduce material ambiguity.
- The graph helper derives relations already present in JSON; it does not discover hidden relations or act as a knowledge store.

### Structured PRD validation

`templates/prd-schema.json` is a JSON Schema Draft 2020-12 artifact schema. `scripts/prd_validate.py` uses Python's standard library and validates the explicitly documented keyword subset used by this repository. It enforces structural and semantic blockers; quality notices are WARN and cannot be used to mask a FAIL. It is **not** a full Draft 2020-12 validator, security approval, vendor allowlist or Harness conformance test.

Run:

```powershell
python .\scripts\prd_validate.py .\templates\market-sample-memory-tools.json
python .\scripts\prd_validate.py --self-test
```

Use a full Draft 2020-12 validator independently when a consumer relies on schema features outside the repository's supported subset.

### Install

The included `install.ps1` targets WorkBuddy by default and accepts a custom skill directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "<your-skills-dir>"
```

Codex discovery and the user's canonical skill directory are documented in the Agent Core integration, not inferred from this WorkBuddy installer.

### Version and governance

Current released Skill baseline: v0.3.2. PRD Intake / Harness alignment work is tracked as **Unreleased** until review, regression and release acceptance pass. Do not bump the version merely because a branch exists.

### License

MIT. Third-party attributions are listed in `NOTICE.md`.

---

## 中文

将模糊意图转化为可审阅的需求。此 Skill 聚焦于**先取证再提问、澄清目标与范围、区分事实/假设/用户决策、定义可观察的验收条件，并形成可追溯的 PRD**。它是需求入口，不是执行 Harness。

### 适用场景

| 场景 | 触发示例 |
|---|---|
| 模糊的软件/产品需求 | “用 grill-to-PRD 帮我明确目标、范围和验收条件。” |
| 调研或技术选型 | “用 grill-to-PRD 梳理调研范围、假设和决策标准。” |
| 跨会话的大型任务 | “先用 wayfinder 拆解目标和决策票据。” |

### 工作流

```
用户意图
   └─ Fast / Deep 需求澄清
          ├─ 先查事实，再向用户提问
          ├─ 分离事实、假设和用户决策
          ├─ 跟踪阻塞/非阻塞未知项
          └─ 生成 PRD 草案 / 确认需求共识
                    └─ 下游 Harness 与领域工作流
```

- **Fast**：只问真正影响目标、范围、成功标准或关键决策的问题。需求已经明确时，零个问题也可能是正确结果。
- **Deep**：使用决策树，每轮用户回答后重新计算当前可澄清问题集合。
- **Wayfinder**：仅用于跨会话或依赖较多的任务；优先复用现有 Issue Tracker，避免重复建账。
- **Draft PRD** 可以保留已明确标注的未知项；标记为 **Ready for plan** 则要求不存在仍未解决的阻塞问题，并取得用户对需求共识的明确确认。

### 治理权威边界

执行规范以 [Harness LOOP Specification v3.1.1](https://github.com/Rain3Dmetrology/agent-harness-loop-spec/blob/84e74b98e628a9358765a261e281fb474018a686/SPEC.zh-CN.md) 为准。本 Skill 只是 Guidance，不实现 TaskContract 生命周期、预算、权限、Effect Approval、Effect Journal、租约、证据有效性、恢复或最终关闭控制。

需求共识不等于计划批准或执行授权。PRD 是需求工件，不是 TaskContract，也不是执行状态 SSOT。字段映射见 `references/harness-interop.md`。

### 输出

- **默认**：`prd-[name].md`，供人审阅。
- **可选**：下游 Agent 或程序需要结构化消费时生成 `prd-[name].json`。
- **可选模块**：User Stories、ADR、需求追踪矩阵、`data_objects`、`pipeline_constraints`、`error_personality` 和 Graph 视图，只在确实减少歧义时启用。
- Graph 工具只派生 JSON 已记录的关系，不会自动发现隐含关系，也不是知识库存储。

### PRD 结构校验

`templates/prd-schema.json` 是 JSON Schema Draft 2020-12 格式的 PRD 工件 Schema。`scripts/prd_validate.py` 使用 Python 标准库，校验仓库明确支持的关键字子集。结构和语义硬错误会阻断；质量建议只报告 WARN，不能用它掩盖 FAIL。它**不是完整的 Draft 2020-12 校验器**，也不是安全审批、供应商许可清单或 Harness 合规证明。

运行：

```powershell
python .\scripts\prd_validate.py .\templates\market-sample-memory-tools.json
python .\scripts\prd_validate.py --self-test
```

下游消费者依赖本仓库支持子集以外的 Schema 功能时，应额外运行完整 Draft 2020-12 校验器。

### 安装

仓库内 `install.ps1` 默认面向 WorkBuddy，同时支持自定义 Skill 目录：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "<your-skills-dir>"
```

Codex 的 Skill 发现路径和用户级目录由 Agent Core 集成部分说明，不从 WorkBuddy 安装脚本推断。

### 版本与治理

当前已发布 Skill 基线为 v0.3.2。PRD Intake / Harness 对齐修改在评审、回归和发布验收完成前均记为 **Unreleased**。不能仅因创建分支就升级版本号。

### 许可证

MIT。第三方来源与许可归属见 `NOTICE.md`。
