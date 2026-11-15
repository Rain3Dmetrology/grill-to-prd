# PRD Intake / Harness 对齐：逐文件修改与验收清单

## 范围与非目标

只修改需求入口 Skill 与 Agent Core 接入，不修改 `agent-harness-loop-spec` v3.1.1 正文，不修改 GitHub 权限治理或发布治理。当前仓库版本号不升级；本变更进入 Unreleased，待 PR 审查、回归和发布验收后再决定版本。

## 文件变更

| 文件 | 优先级 | 改动 | 验收 |
|---|---|---|---|
| `SKILL.md` | P0 | 删除复制的 v2.3 权威块；声明 Skill=Guidance；区分需求共识、计划冻结、执行授权和 human closure；允许 Draft 与 ready_for_plan 两种状态 | 不再把 B1-B7/R4/R7/E0-E3/G1-G3 宣称为规范控制；Skill 不承担执行生命周期 |
| `references/harness-interop.md` | P0 | 新增 PRD → Harness v3.1.1 字段映射与权限边界 | 目标、范围、验收、事实、假设、人工接受均有映射；不声称 PRD 可授权执行 |
| `templates/prd-schema.json` | P0 | 变为 Draft 2020-12 JSON Schema | 标准 schema 可被通用 JSON Schema 工具读取；必填字段和字段类型明确 |
| `scripts/prd_validate.py` | P0 | 删除评分覆盖 FAIL 的行为；结构/语义错误硬失败；quality warnings 不阻断；防御 malformed collections | 自测覆盖 Draft 未决问题允许、ready_for_plan 正反例、重复 ID、未知字段、空验收、human_acceptance closure、已接受 ADR 至少两个备选 |
| `templates/prd-template.md` | P1 | 移除固定三验收门、≥10 stories、强制 ledger；Markdown 默认 | 简单任务可裁剪；验收类型与 closure 分离 |
| `references/domain-adapters.md` | P1 | 将 source allowlist 限定为来源适用性指导 | 不把来源列表描述成网络或供应商权限；保留领域事实源选择能力 |
| `scripts/graph_derive.py` | P1 | 兼容 schema 1.0 的 facts/requirements/acceptance/assumptions/decisions/open_questions/relations；保留旧输入只读兼容 | flat 视图覆盖当前核心需求字段；graph 只读取显式 relations，不声称自动发现关系 |
| `.github/workflows/prd-validation.yml` | P2 | 自动运行脚本编译、validator 自测、迁移样例校验和 graph JSON 冒烟测试 | GitHub Actions PR check 全绿；不能替代完整 JSON Schema conformance 或 Codex 本地发现测试 |
| `docs/phase5-factcheck.json` | 兼容性说明 | 保留为历史 v0.3.x 记录，不自动改写 | 历史记录不被误当作 schema 1.0 fixture；需迁移后方可用于当前 validator |
| `README.md` / `CHANGELOG.md` | P1 | 同步治理边界、默认输出、validator 语义与 Unreleased 记录 | 不再声称旧 v2.3 是执行权威或评分≥80即可放行 |
| `templates/*sample*.json` | P1 | 迁移示例至 schema_version 1.0；旧事实标记 unverified，迁移注记放入 `extensions` | 样例符合当前 root schema；历史事实不伪装为当前证据 |

## P0/P1 顺序

1. 权威与职责边界。
2. 正式 JSON Schema 与不会误放行的 validator。
3. 模板、适配器、README/CHANGELOG 与样例迁移。
4. Agent Core 注册与 Codex 用户级目录适配。
5. CI/held-out 测试集与真实 Codex 运行验收；未实测前不得称 Codex 已通过。

## 验收边界

GitHub Actions workflow 对 Python 3.11 完成语法编译、validator self-test、两个 schema 1.0 样例和 graph JSON 冒烟测试。Validator self-test 只证明脚本逻辑覆盖列出的用例，不证明完整 JSON Schema Draft 2020-12 实现、Codex 发现行为或 Harness C1/C2 合规。仓库 validator 只实现 README 明示的 JSON Schema 关键字子集；完整 schema 兼容性需由通用 Draft 2020-12 validator 独立验证。旧版 `docs/phase5-factcheck.json` 保留其历史语境，不属于当前 schema 1.0 回归夹具。