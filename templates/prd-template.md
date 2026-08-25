# PRD: [需求/项目名]

> 结构对齐 prd-master 11 节（按场景裁剪映射，见 SKILL.md §6.3）；优先级用 MoSCoW/RICE/Kano 框架；验收标准用 BDD Given-When-Then 或 Checklist 双格式。

## B1 主目标（冻结 · 不可变）
- 目的（用户原话）：
- IN scope：
- OUT of scope：

## B2 验收门（每门附验收命令 + 验收挂载点）
| 门 | 定义 | 验收命令 | 验收挂载点 | 最低证据 | 状态 |
|---|---|---|---|---|---|
| G1 单元/局部 | | | | E1 | 待办 |
| G2 集成 | | | | E2 | 待办 |
| G3 实机/Live | | | | E3+用户确认 | 待办 |

> 验收挂载点（v0.3.0 seams 推广）：代码域=测试缝隙（seam，理想=1）；市场域=数据源交叉验证点（≥2 独立源）；生活域=关键检查点。

## 结束条件三态
- 达标即停 / 预算耗尽即停 / 最多 N 轮（默认 N=5）

## 一、Executive Summary（执行摘要）
- Problem Statement（2-3 句，从用户视角；Problem Before Solution 硬规则）
- Proposed Solution（1-2 句）
- Success Metrics（3-5 个可量化指标，No Vague Metrics 硬规则）

## 二、Context & Background（背景）
- 为什么现在做？（市场机会/用户痛点/生活场景背景）
- 战略对齐 / 相关背景
- 不做的后果

## 三、Goals & Success Metrics
### Business/User Objectives
- 业务/用户目标（可量化）

### Success Criteria（成功标准表）
| 指标 | 当前值 | 目标值 | 测量方式 |
|---|---|---|---|
| | | | |

## 四、Target Users / Personas（目标用户/相关方）
- 主要用户/相关方（谁受益最大）
- 次要用户/间接受益者
- 需求、痛点、动机（Jobs to be done）

## 五、User Stories（LONG 列表 · INVEST 合规 · per-US 优先级）
> 数量要求（v0.3.0）：≥10 条或覆盖全部功能面，极尽详尽；每条过 INVEST 检查（Independent/Negotiable/Valuable/Estimable/Small/Testable）。

### [编号]: [标题]（优先级: P0/P1/P2 或 MoSCoW 类别）
**Description:** 作为 [角色]，我想要 [能力]，以便 [收益]。
**Acceptance Criteria（BDD Given-When-Then 或 Checklist）:**
- [ ] Given [前置条件] / When [动作] / Then [预期结果]
- [ ] （含 happy path + edge cases）

## 六、Requirements（需求）
### Functional Requirements（FR）
- FR-1: ...
### Non-Functional Requirements（NFR）
- NFR-1: 性能/安全/可用性（全部可量化）

## 七、Out of Scope（明确不做什么）
- 明确 NOT building
- 未来阶段考虑项

## 八、执行决策 / 验证决策（v0.3.0）
> 场景映射：代码=Implementation/Testing Decisions；市场=执行策略/验证方法；生活=实施方案/验收方式。

### 执行决策（Implementation Decisions）
- 模块/接口/架构决策（不含具体文件路径）
- 备选方案论证（Alternatives Required：至少 2 个备选 + Pros/Cons/Decision）

### 验证决策（Testing Decisions）
- 验收挂载点 + 验证方法
- 测试范围与先例

## 九、决策记录（不可逆抉择 → ADR）
> ADR 模板（v0.3.0 升级）：必须含备选方案论证。

### ADR-XXX: [决策标题]
- **Context**：背景与约束
- **Decision**：决定（选哪个方案）
- **Alternatives Considered**（≥2 备选 + Pros/Cons/Decision）
- **Consequences**：后果与代价
- **Status**：Proposed / Accepted / Deprecated

## 十、需求追踪矩阵（v0.3.0 · 可追溯性）
| 需求 | 设计元素 | 实现 | 测试/验收 |
|---|---|---|---|
| US-001 | | | G1 验收命令 |

## 十一、约束与边界收敛
| 维度 | 收敛结果 | 证据等级 |
|---|---|---|
| 范围 | | |
| 时间 | | |
| 成本 | | |
| 质量优先级排序 | | |
| 技术/领域约束 | | E1 |
| 兼容性 | | E1 |
| 可验证量化 goal | | |
| 取舍优先级（MoSCoW/RICE/Kano 裁决） | | |
| 受信任检索域名 | | |
| 性能/质量要求 | | E1 |

## 十二、Rollout / 实施计划
- 分阶段策略
- 里程碑 + Feature flags/A-B（如适用）
- 回滚计划（如适用）

## 十三、Open Questions & Risks
- 遗留待澄清项（open questions）
- 风险与缓解（| 风险 | 严重度 | 可能性 | 缓解 |）
- 对其他事项的依赖
