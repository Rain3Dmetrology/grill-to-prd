# PRD: [功能/项目名]

## B1 主目标（冻结 · 不可变）
- 目的（用户原话）：
- IN scope：
- OUT of scope：

## B2 验收门（每门附验收命令）
| 门 | 定义 | 验收命令 | 最低证据 | 状态 |
|---|---|---|---|---|
| G1 单元/局部 | | | E1 | 待办 |
| G2 集成 | | | E2 | 待办 |
| G3 实机/Live | | | E3+用户确认 | 待办 |

## 结束条件三态
- 达标即停 / 预算耗尽即停 / 最多 N 轮（默认 N=5）

## 一、Introduction / 问题陈述
（要解决的问题，从用户视角）

## 二、Goals
（可验证、可量化的目标，bullet 列表——"P95 延迟 < 200ms"而非"性能提升"）

## 三、User Stories
### US-001: [标题]
**Description:** As a [user], I want [feature] so that [benefit].
**Acceptance Criteria:**
- [ ] 可验证标准（非"工作正常"）

## 四、Functional Requirements
- FR-1: ...

## 五、Implementation Decisions（Deep 模式）
（架构决策/API 契约/Schema 变更；不含文件路径。不可逆抉择须有 ADR 引用）

## 六、Testing Decisions
（seams 测试挂载点 = G 门验收命令的挂载位置；理想 seam 数 = 1）

## 七、约束与边界收敛
| 维度 | 收敛结果 | 证据等级 |
|---|---|---|
| 范围 | | |
| 时间 | | |
| 成本 | | |
| 质量优先级排序 | | |
| 技术约束 | | E1 |
| 兼容性 | | E1 |
| 可验证量化 goal | | |
| 取舍优先级 | | |
| 受信任检索域名 | | |
| 性能要求 | | E1 |

## 八、Non-Goals / Out of Scope
（明确不做什么）

## 九、Success Metrics
（如何衡量成功）

## 十、Open Questions
（遗留待澄清项）
