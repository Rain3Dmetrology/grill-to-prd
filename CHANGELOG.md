# Changelog

All notable changes to grill-to-PRD are documented here.
本文件名不含版本号（R1 教训），版本演进仅记录于本文件。

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
