# Changelog

All notable changes to grill-to-PRD are documented here.
本文件名不含版本号（R1 教训），版本演进仅记录于本文件。

## [v0.3.2] - 2026-08-27

### Added（补装缺口① + 缺口②，源自 PRD skill 选型调研落地方案）
- **缺口① 程序化 PRD 校验门禁**：`scripts/prd_validate.py`（零依赖纯标准库）——四维检查（目标可量化性 25 / 边界清晰度 25 / 测试缝隙 25 / 技术合规性 25）+ 0-100 评分 + 逐条修复指令（"错误信息=修复指令"）。评分 ≥80 才流转下游（对齐 Google 方案一阶段三，平台无关版）；技术合规性默认 WARN 扣分（日常检索友好，白名单含开发基础设施+搜索引擎），加 `--compliance-strict` 升级为 HARD-FAIL 硬门禁。支持 prd-*.json（逐字段断言）与 prd-*.md（启发式）双输入，含 --self-test。
- **缺口② 面向 Agent 的三模块**：`prd-schema.json` 新增 `data_objects`（实体数据字典+状态机）/ `pipeline_constraints`（Pipeline 拓扑约束）/ `error_personality`（异常降级人格）三字段；`prd-template.md` 新增十之一~十之三章节；SKILL.md §6.3 增加「面向 Agent 的三模块」说明（按需追加，非每篇硬塞）。

### Changed（发布前同步）
- README 重构为**中英对照双语版**（`[English](#english) | [中文](#中文)` 单文件锚点结构，段落对齐，155 行 ≤ 200 行预算），补录 v0.3.2 特性与目录表；修复 install 示例路径空格。
- 清除 CHANGELOG/docs 中泄露的本机磁盘路径（用户特定盘符路径）；`.gitignore` 补强凭据类文件覆盖（.env/*.key/credentials*/local_*_paths* 等）。

### Notes
- 依据：《PRD需求引导skill选型调研_终审报告_v1.0》落地方案（缺口① prd_validate.py + 缺口② 三模块 schema）。
- 三模块为按需追加：凡涉多实体状态流转/多模块依赖/AI 或搜索类异常的场景启用，简单 flat 需求可省。

## [v0.3.1] - 2026-08-26

### Changed（终局审计修复：P0/P1/P2 全量）
- **P0-1 R13 同步 v2.3**：§0 内嵌 R13 补全 d 款（无标记静默截断三兜底：量纲核对/结构完备校验/双路取回比对）+ f 款完整表述（全测或抽样≥3 并标注抽样率与未测项）——修复"内嵌规则漂移"（防漂移的技能自己先漂了）。
- **P1-1 内嵌对齐锚点**：§0 新增「内嵌对齐」声明（对齐治理规范 v2.3 2026-08-25；同步触发=规范 bump + 季度审计）。
- **P2 分层内嵌架构**：§0 治理权威块重构为三层——稳定内核逐字内嵌（B1/B2/E0-E3/三态/R4/R7/Hard Rules）／高频演进条款引用摘要（R13 a-g）／阶段专属引用指向（R9 心跳/确认分级/触顶上报/M1-M11 由下游 harness 承担）——根治"内嵌 vs 引用"张力。
- **P1-4 C/P 职责边界声明**：§1 新增——本 skill 负责 C（澄清）+P（计划）阶段，不承担 E/V/L/多智能体派发（防范围蔓延）。

### Added
- **P1-2 install.ps1 原子化**：临时目录 + 原子改名 + 失败回滚保留旧版（对齐治理 R4 原子写精神）。
- **P2-1 R7 双层持久内嵌**：§0 稳定内核层补 R7（会话重发=缓存层，任务级落盘 ledger.md 为准）。
- **30 秒上手**：SKILL.md 与 README 顶部新增三场景触发示例（技术选型/市场调研/生活决策）。
- **维护契约**：README 新增——治理规范 bump 与 mattpocock 上游更新的手动同步纪律；未经 L 复盘或用户确认不 bump 版本。

### Notes
- 依据：《grill-to-PRD终局审计_符合性与完善建议_2026-08-26.md》（1 P0 + 4 P1 + 架构级隐患，经用户确认全量执行）
- v0.3.0 升级未走正式 L 复盘已补做（见 memory L 区块）

## [v0.3.0] - 2026-08-26

### Changed（对齐 mattpocock 原教旨 + 五资产吸收）
- **三段式架构声明（§1）**：wayfinder（规划器·超长任务）→ grilling（追问器·多轮设计树）→ to-spec（合成器·单次不追问），grill-to-PRD 为统一入口 + 治理胶水。认知纠偏：to-spec 是纯合成器（原文 disable-model-invocation + "Do NOT interview"）；wayfinder 是域无关规划器（原文 "domain-agnostic"）。
- **追问轮次门禁（§3.1）**：frontier 空证明（全部未决决策逐条标注已 settle/待用户/待取证）+ 用户共识确认门 + 每轮格式对齐 grilling 原文（编号+推荐答案）+ 短任务豁免。
- **pre-fact 前置（§3.2）**：每个 frontier 问题先自问"能否自己查"——能则先取证再提问，并行探索子代理不阻塞。
- **wayfinder 规划（§3.4）**：超长任务入口（命名目的地→测绘前沿→决策票据地图→逐票据解决→本地 markdown tracker 轻量落地）。
- **命名修正（§2）**：Deep/Fast → 深度/快速模式（追问强度分级，与领域无关）。
- **prd-master 三条 Hard Rules（§0）**：No Vague Metrics / Problem Before Solution / INVEST Stories。
- **优先级框架（§7 + 模板）**：MoSCoW/RICE/ICE/Kano + Hybrid 组合法替换简单 P0/P1/P2；落地三件套（per-US 优先级 + 取舍裁决表 + goal 可量化强制）。
- **守卫与机检（§9）**：vibeguard 模式（规则/钩子/静态检查三层 + "错误信息=修复指令" + learn 闭环 5-Why→新守卫）。

### Added
- 领域适配器扩展至 6 个：新增**商业模式**与**日常生活**适配器 + 百科型事实源模式（§5 + domain-adapters.md）
- 11 节 PRD 结构（prd-template.md，对齐 prd-master，按场景裁剪映射）+ BDD Given-When-Then/Checklist 验收双格式
- ADR 模板升级：Alternatives Required（≥2 备选方案 + Pros/Cons/Decision，源自 technical-spec）
- 需求追踪矩阵 REQ→Design→Impl→Tests（prd-template §十 + schema，to-tickets 上游输入）
- 验收挂载点（seams 推广：代码=seam / 市场=数据源交叉验证点 / 生活=关键检查点）
- prd-schema.json 新字段：gates.mount_point / priority.framework / user_stories.priority + invest / execution_decisions / verification_decisions / adrs.alternatives_considered / traceability_matrix

### Notes
- v0.4.0 候选架构（规划未实施）：skill-router 形态（routing.json 结构化路由 + 173 用例式回归基准 + field-journal 经验库）——源自 reverse-skill 范式
- 诊断与洞察报告：《grill-to-PRD追问机制诊断与v0.3.0升级建议_2026-08-26》《grill-to-PRD五资产对照调研与v0.3.0增补洞察_2026-08-26》

## [v0.2.1] - 2026-08-25

### Changed（对齐审计裁决落地）
- **Fast 模式（R1/R2）**：只强制收敛 3 项（目标/范围/验收标准），其余标「待定」进 open_questions；精简治理（只 B1 冻结 + 验收标准可验证，跳过 E0-E3/R13/台账）。
- **核心边界（R3）**：核心 = 引导 + 双形态输出；领域适配层/专家团衔接/to-tickets = 可选挂载。

### Added
- codebase 适配器补充 deepwiki MCP 取证（快速索引 E1）+ seams 取证（D4）
- 市场调研样例 `templates/market-sample-memory-tools.json`（D5，harness agent 记忆智能体热门工具盘点）
- 对齐审计报告 `docs/对齐审计-v0.2.0.md`

### Fixed
- README/prd-template 文档漂移（通用化同步）
- MEMORY.md 过时技术假设回写（C++17/PCL 1.10/Phase 5 完成）

## [v0.2.0] - 2026-08-25

### Changed
- **定位升级为通用需求引导翻译官**：不绑定代码仓库/具体领域，可服务于任意"模糊→清晰"需求场景（软件开发/调研分析/产品规划/技术选型），并可作为专家/专家团的需求入口。
- Deep 模式去代码绑定：事实取证从"代码库"扩展为**通用多信息源**（fact 归 agent 机制保持）。
- 新增 **§5 领域适配层** + `references/domain-adapters.md`：核心通用，领域差异（代码库/HF/市场/专利）通过适配器注入；内置 4 个适配器 + 自定义模板。
- 新增 **§8 专家团衔接**：PRD 产出直接映射为专家团研究参数卡/来源池/验收门输入。

### Added
- references/domain-adapters.md（领域适配器机制 + 内置 4 适配器 + 自定义模板）
- 通用化定位说明（SKILL.md §1）

### Notes
- 三源 attribution 见 NOTICE.md（MIT ×2 + Apache-2.0 ×1）
- 治理规范升级时手动同步内嵌规则（不跨仓库 pin）

## [v0.1.0] - 2026-08-25

### Added
- 初始脚手架：SKILL.md 五段式（治理权威声明 + 意图路由 + Deep/Fast/HF 三模式 + 输出层 + 边界收敛清单）
- Deep 模式内核：移植 mattpocock/skills 的 grilling（设计树+frontier+分轮）+ domain-modeling（glossary+ADR 三触发）+ to-spec（seams+模板）
- Fast 模式内核：移植 snarktank/ralph 的 Lettered Options + PRD 模板
- HF 场景：移植 huggingface/skills 的 huggingface-best（benchmark+device 预算）+ 复用 HF MCP 取证
- 合规胶水：内嵌 v2.3 规则（B1/B2 验收命令先行/结束条件三态/证据分级 E0-E3/R13 截断防护）
- 输出层：JSON+Markdown 双形态 + flat/graph 分层
- scripts/graph_derive.py（零依赖 graph 派生）
- templates/prd-schema.json + prd-template.md

### Notes
- 三源 attribution 见 NOTICE.md（MIT ×2 + Apache-2.0 ×1）
- 治理规范升级时手动同步内嵌规则（不跨仓库 pin）
