# grill-to-PRD — 通用需求引导翻译官

把模糊意图翻译成结构化 PRD。核心不是写文档，而是**动手前把话说透、把假设暴露、把验收门钉死、把边界收敛**。遵守《人机协作 Loop 治理规范》v2.3。
**通用定位**：领域无关的需求引导引擎——软件开发、调研分析、产品规划、技术选型等任意场景，也可作为专家/专家团的需求入口。

## 双模式 + 领域适配层

| 模式 | 场景 | 内核 |
|---|---|---|
| **Deep** | 深度/高风险/多决策/需沉淀不可逆抉择 | grilling 设计树 + 决策留痕（ADR + 术语表） |
| **Fast** | 快速固化需求边界+验收标准、最小交互 | Lettered Options（1A,2C,3B 批量） |
| **领域适配层** | 特定领域事实密集（代码库/HF/市场/专利…） | `references/domain-adapters.md` 适配器注入 |

## 输出

- 双形态：`prd-[name].md`（叙事）+ `prd-[name].json`（结构）
- 分层：flat list（事实）/ graph（关系，`scripts/graph_derive.py` 派生）
- 台账：`ledger.md` + `ledger.json`
- 下游：软件开发场景可续 to-tickets；调研场景作为专家团任务卡/参数卡输入

## 安装（WorkBuddy skill 格式）

1. 复制本目录到你的 skill 目录（或作为独立仓库 clone）。
2. 脚本用**相对路径**调用，平台无关（WorkBuddy / Trae / Codex 通用）。

## 依赖

- 零运行时依赖（脚本仅标准库）。
- 领域适配器可选复用对应连接器（如 HF 场景复用 HuggingFace MCP 取证 E1）。

## License

MIT。第三方 attribution 见 `NOTICE.md`（mattpocock/skills MIT、snarktank/ralph MIT、huggingface/skills Apache-2.0）。

## 目录

```
SKILL.md            主入口（通用需求引导 + 内嵌 v2.3 合规规则 + 领域适配层 + 专家团衔接）
LICENSE / NOTICE.md 许可证与三方 attribution
CHANGELOG.md        版本史（文件名去版本化，版本存此）
references/         领域适配器（domain-adapters.md：代码库/HF/市场/专利）
scripts/            零依赖脚本（graph_derive.py · truncation_lint.py）
templates/          输出模板（prd-template.md · prd-schema.json）
docs/               实测与验证记录
```
