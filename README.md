# grill-to-PRD — 需求引导翻译官

把模糊意图翻译成结构化 PRD。核心不是写文档，而是**动手前把话说透、把假设暴露、把验收门钉死**。遵守《人机协作 Loop 治理规范》v2.3。

## 双模式

| 模式 | 场景 | 内核 |
|---|---|---|
| **Deep** | 代码库深度绑定、架构/技术选型、需沉淀领域名词与不可逆抉择 | grilling 设计树 + ADR + seams |
| **Fast** | 快速固化需求边界+验收标准、最小交互 | Lettered Options（1A,2C,3B 批量） |
| **HF** | 模型/数据集选型 | benchmark 比较 + device 参数预算 |

## 输出

- 双形态：`prd-[name].md`（叙事）+ `prd-[name].json`（结构）
- 分层：flat list（事实）/ graph（关系，`scripts/graph_derive.py` 派生）
- 台账：`ledger.md` + `ledger.json`
- 下游：to-tickets（tracer-bullet 任务拆分），止于此不碰 implement

## 安装（WorkBuddy skill 格式）

1. 复制本目录到你的 skill 目录（或作为独立仓库 clone）。
2. 脚本用**相对路径**调用，平台无关（WorkBuddy / Trae / Codex 通用）。

## 依赖

- 零运行时依赖（脚本仅标准库）。
- HF 场景可选复用已连接的 HuggingFace MCP（取证 E1）。

## License

MIT。第三方 attribution 见 `NOTICE.md`（mattpocock/skills MIT、snarktank/ralph MIT、huggingface/skills Apache-2.0）。

## 目录

```
SKILL.md            主入口（路由 + 双模式 + 内嵌 v2.3 合规规则）
LICENSE / NOTICE.md 许可证与三方 attribution
CHANGELOG.md        版本史（文件名去版本化，版本存此）
scripts/            零依赖脚本（graph_derive.py · 相对路径）
templates/          输出模板（prd-template.md · prd-schema.json）
```
