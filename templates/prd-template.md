# PRD: [需求/项目名]

> 按任务规模裁剪。默认输出 Markdown；只有下游需要结构化消费时才生成 JSON。
> 需求共识、计划冻结、执行授权和最终接受是不同事件，不得混用。

## 1. 目标与边界
- 用户目的（尽量保留原意）：
- IN scope：
- OUT of scope：
- 成功结果 / 可观察指标：

## 2. 背景与问题
- 当前问题：
- 受影响用户/相关方：
- 为什么现在处理：
- 当前基线及其来源：

## 3. 需求
### 功能需求
| ID | 需求 | 优先级 | 来源/理由 |
|---|---|---|---|
| REQ-001 | | Must/Should/Could/Won't | |

### 非功能需求（按需）
| ID | 质量属性 | 可观察标准/测量方式 |
|---|---|---|
| NFR-001 | | |

## 4. 验收条件
| ID | 验收条件 | 验证方法 | 预期结果 | 类型 | 阶段 |
|---|---|---|---|---|---|
| ACC-001 | | automated_test / manual_review / benchmark / data_check / inspection / other | | deterministic / semantic / human_acceptance / physical | verification / closure |

> 不强制 G1/G2/G3 三层。需要用户最终接受的条件单列为 human_acceptance，且属于 closure；物理/实机验证仍是独立验证证据。

## 5. 已知事实、来源与假设
| ID | 陈述 | 状态 | 来源/获取时间 | 限制 |
|---|---|---|---|---|
| F-001 | | observed / inferred / unverified | | |

| 假设 ID | 假设 | 状态 | 影响 | 验证方式 |
|---|---|---|---|---|
| ASM-001 | | accepted / unverified / rejected | | |

## 6. 决策与取舍
| ID | 决策问题 | 选项 | 当前选择 | 负责人 | 状态 |
|---|---|---|---|---|---|
| DEC-001 | | | | user / agent / policy | open / accepted / rejected / deferred |

只有长期或高影响决策才建立 ADR；确需 ADR 时，记录上下文、至少两个可行替代方案、取舍和后果。

## 7. User Stories / Use Cases（按需）
仅在使用 user-story 形式时检查 INVEST；条目数量以功能覆盖为准，不设置固定最低数量。

## 8. 数据、流程与异常扩展（按需）
- data_objects：实体、关键属性、状态及合法转移
- pipeline_constraints：模块依赖、执行顺序和数据流
- error_personality：异常信号、降级动作和恢复路径

## 9. 范围外事项、风险与待确认问题
- 明确不做的事项：
- 风险及缓解：
- 阻塞性问题：
- 非阻塞性问题：

## 10. 需求状态
- [ ] Draft：仍有未知项，但已显式记录
- [ ] Ready for plan：阻塞问题已解决/明确接受为假设，用户确认需求共识

> Ready for plan 仅代表需求表达已确认，不代表计划已批准、TaskContract 已冻结或执行权限已授予。
