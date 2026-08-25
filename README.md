# grill-to-PRD — 通用需求引导翻译官

把模糊意图翻译成结构化 PRD。核心不是写文档，而是**动手前把话说透、把假设暴露、把验收门钉死、把边界收敛、把优先级排清**。遵守《人机协作 Loop 治理规范》v2.3。
**通用定位**：**域无关**的需求引导引擎——软件开发、产品规划、市场商业、技术/模型选型、日常生活任意场景，也可作为专家/专家团的需求入口。

## 三段式架构（v0.3.0 · 对齐 mattpocock/skills 原教旨）

```
wayfinder（规划器 · 域无关）  大型模糊任务 → 决策票据地图 → 逐票据解决（超长任务入口）
grilling（追问器 · 域无关）   多轮 frontier 设计树：整前沿+推荐答案+重算，frontier 空才停
to-spec（合成器 · 域无关）    单次合成（不追问）→ PRD：LONG stories + 执行/验证决策 + 验收挂载点
grill-to-PRD = 统一入口 + 治理胶水（B1-B7 台账 / G1-G3 验收门 / E0-E3 证据分级 / 双形态输出）
```

## 双模式 + 领域适配层（v0.3.0 命名修正）

| 模式 | 场景 | 内核 |
|---|---|---|
| **深度模式**（原 Deep） | 深度/高风险/多决策/需沉淀不可逆抉择 | grilling 多轮设计树 + **轮次门禁（frontier 空证明）+ 用户共识确认门** + 决策留痕（ADR + 术语表） |
| **快速模式**（原 Fast） | 快速固化需求边界+验收标准、最小交互 | Lettered Options（1A,2C,3B 批量）+ MoSCoW 轻量优先级 |
| **wayfinder 规划** | 任务超一个会话 | 目的地→测绘前沿→决策票据地图→逐票据解决（本地 markdown tracker 轻量落地） |
| **领域适配层** | 特定领域事实密集 | `references/domain-adapters.md` 适配器注入（**6 个**：代码库/HF/市场/专利/商业模式/日常生活） |

> 深度/快速是**追问强度分级**，与领域无关；领域差异一律走适配层。

## 核心能力（v0.3.0）

- **追问质量三 Hard Rules**：No Vague Metrics（指标必须可量化）/ Problem Before Solution（先定义问题）/ INVEST Stories
- **优先级框架**：MoSCoW / RICE / ICE / Kano + Hybrid 组合法；per-US 优先级（P0/P1/P2）+ 取舍裁决表 + goal 可量化强制
- **PRD 结构**：11 节（对齐 prd-master，按场景裁剪映射）+ BDD Given-When-Then/Checklist 验收双格式
- **决策留痕**：ADR 强制 ≥2 备选方案（Alternatives Required）+ 需求追踪矩阵 REQ→Design→Impl→Tests
- **验收挂载点**（seams 推广）：代码=测试缝隙（seam）/ 市场=数据源交叉验证点 / 生活=关键检查点
- **守卫与机检**：vibeguard 模式三层守卫（规则/钩子/静态检查）+ learn 闭环（5-Why 根因→新守卫）+ `truncation_lint.py` 截断机检

## 输出

- 双形态：`prd-[name].md`（叙事）+ `prd-[name].json`（结构，schema 见 `templates/prd-schema.json`）
- 分层：flat list（事实）/ graph（关系，`scripts/graph_derive.py` 派生，零依赖）
- 台账：`ledger.md` + `ledger.json`
- 下游：软件开发场景可续 to-tickets（追踪矩阵为上游输入）；调研场景作为专家团任务卡/参数卡输入

## 安装

### WorkBuddy（用户级，推荐）

```powershell
# 一键安装到 WorkBuddy 默认技能目录（~/.workbuddy/skills/grill-to-prd）
powershell -ExecutionPolicy Bypass -File .\install.ps1
# 自定义目标目录：
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "C:\Users\<你>\ .workbuddy\skills"
```

> 版本漂移防护（R1 教训）：install.ps1 每次安装会打印源版本（CHANGELOG 最新条目）与已安装副本版本；升级后重跑 install.ps1 即可同步。脚本相对路径调用，平台无关（WorkBuddy / Trae / Codex 通用）。

### 手动复制 / clone

1. 复制本目录到你的 skill 目录（或 clone 独立仓库）。
2. 脚本用**相对路径**调用，平台无关。

## 依赖

- 零运行时依赖（脚本仅 Python 标准库）。
- 领域适配器可选复用对应连接器（如 HF 场景复用 HuggingFace MCP 取证 E1；代码库场景可选 deepwiki MCP 快速索引）。

## License

MIT。第三方 attribution 见 `NOTICE.md`（mattpocock/skills MIT、snarktank/ralph MIT、huggingface/skills Apache-2.0）。

## 目录

```
SKILL.md            主入口（三段式架构 + 内嵌 v2.3 合规规则 + Hard Rules + 守卫机检 + 6 适配器 + 专家团衔接）
LICENSE / NOTICE.md 许可证与三方 attribution
CHANGELOG.md        版本史（文件名去版本化，版本存此）
install.ps1         一键安装到 WorkBuddy 技能目录（含版本漂移提示）
references/         领域适配器（domain-adapters.md：6 个内置 + 百科型事实源模式 + 自定义模板）
scripts/            零依赖脚本（graph_derive.py · truncation_lint.py）
templates/          输出模板（prd-template.md · prd-schema.json · 自测样例×2）
docs/               实测与验证记录（含 v0.3.0 升级自审报告）
```
