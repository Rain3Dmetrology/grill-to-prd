# Changelog

All notable changes to grill-to-PRD are documented here.
本文件名不含版本号（R1 教训），版本演进仅记录于本文件。

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
- 诊断与洞察报告：`D:\Downloads\grill-to-PRD追问机制诊断与v0.3.0升级建议_2026-08-26.md`、`D:\Downloads\grill-to-PRD五资产对照调研与v0.3.0增补洞察_2026-08-26.md`

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
