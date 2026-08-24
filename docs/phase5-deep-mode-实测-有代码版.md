# grill-to-PRD Deep 实测（有代码在盘）：rxs-cc-plugins 命名空间与 API 对齐盘点

**实测目的**：补跑"有代码在盘"的 Deep 模式，验证 fact 取证闭环 + 沉淀领域名词关系图与不可逆抉择。
**代码源**：`https://github.com/rxsvision/rxs-cc-plugins.git`（已 clone 至 D:\Downloads\rxs-cc-plugins）
**工具链**：grep 取证（E1）+ `scripts/graph_derive.py` 派生 + ADR 三触发判据 + 验收门 G1-G3
**日期**：2026-08-25

---

## 一、取证过程（全部 E1：真代码，非假设）

| # | 取证项 | 命令/位置 | 结果 |
|---|---|---|---|
| F1 | rxs:: 命名空间 | grep `namespace rxs\|rxs::` 全仓库 | **0 处** |
| F2 | 实际命名空间 | czxDependence/czxTool.h:402,467 | `namespace arsenal` / `namespace czxEigen`（另有 `using namespace std/Eigen`） |
| F3 | C++ 标准 | CMakeLists.txt:4 | `set(CMAKE_CXX_STANDARD 17)` = **C++17** |
| F4 | 导出宏 | grep `RXS_EXPORT\|__declspec\|_EXPORT` | **0 处** |
| F5 | 插件接口 | grep `ccStdPluginInterface\|Q_PLUGIN_METADATA` | **0 处** |
| F6 | 仓库形态 | 目录结构 | 独立 VS 工具集（.sln/.vcxproj + czxDependence），mesh2cad（delaunay + pcd2stl）、meshSlice（源.cpp） |

## 二、假设 vs 现实：3 处被真代码推翻（实测核心价值）

| memory 假设（无代码在盘的实测输入） | 真代码事实 | 影响 |
|---|---|---|
| 命名空间统一 `rxs::`（曾 vision3d::） | **此仓库无 rxs::、无 vision3d::**，实际是 arsenal/czxEigen | **rxs-cc-plugins 可能不是 rxs:: 改造目标，或改造未开始**——若按假设对错仓库做改造，返工灾难 |
| C++20 基线 | **C++17**（CMakeLists 明确） | 对齐改造前需先明确各仓库标准差异 |
| 有 rxs_export.h / rxs_api.h / API 层 | **无导出宏、无 API 层**，是独立工具集 | Phase 5 的"API 层改造"对象在别的仓库（rxs-toolkit/algorithms） |

## 三、真实领域名词（从代码提取）

`arsenal`（工具命名空间）· `czxEigen`（Eigen 封装）· `czxDependence`（工具库）· `pcd2stl`（点云→STL）· `delaunay`（三角化）· `meshSlice`（切片）· `rxs_mesh2cad`（项目名，仅名字带 rxs）

## 四、真实不可逆抉择 ADR（三触发条件判据）

### ADR：arsenal/czxEigen 是否并入 rxs::？（待用户裁决，因触发条件部分满足）
- **难逆转** ✅：合并命名空间 = 全仓库重命名 + 下游引用改动
- **无上下文会惊讶** ✅：arsenal/czxEigen 是历史命名，无品牌关联
- **真实取舍** ✅：并入 rxs::（统一品牌）vs 保留 arsenal/czxEigen（最小改动、独立工具库可复用）
- **状态**：三条件满足 → **建议写 ADR，但"是否并入"本身是用户的不可逆抉择，skill 只能提示不能代决**（decision 归用户）

### ADR：C++17 基线（此仓库）vs C++20（rxs-toolkit 假设）
- 三条件部分满足，但**证据不足**（只知道本仓库 C++17，不知道其他仓库标准）→ 按判据**不写 ADR**，先取证

> 这验证了 ADR 三触发条件的**克制价值**：它阻止了"对证据不足的决策盲目写 ADR"——正是你要的"避免过度约束"。

## 五、关系图（`graph_derive.py` 真实跑出）

```
graph LR
    rxs_cc_plugins -->|depends_on| arsenal命名空间
    rxs_cc_plugins -->|depends_on| czxEigen命名空间
    arsenal命名空间 -.->|constrained_by| C1_czxDependence依赖
    rxs_cc_plugins -.->|constrained_by| C++17标准
    rxs_cc_plugins ==>|locked_by| Phase5对齐判定G3
```

## 六、验收门（真实）

| 门 | 定义 | 验收命令 | 证据 |
|---|---|---|---|
| G1 取证完整 | 4 类取证覆盖 | grep 已跑 | E1 ✅ |
| G2 假设对账 | memory 假设逐条对账 | 本报告 §二 | E2 ✅ |
| G3 对齐判定 | rxs-cc-plugins 是否属 rxs:: 改造目标 | **用户裁决** | E3 ⏳ |

## 七、实测结论（刻薄自评）

**验证通过的（skill 框架成立）**：
1. **"fact 归 agent"机制的价值被实证**——真代码推翻了 3 个 memory 假设。若无代码在盘实测就按假设做 Phase 5，会对错误对象做改造。这是 grill-to-PRD 相对"纯对话澄清"的**核心增量**：澄清不只是问用户，而是 agent 先自己取证、再带着事实问决策。
2. **ADR 三触发判据的克制性被验证**——它拒绝了"对证据不足的决策写 ADR"，防止过度治理。
3. **graph_derive.py 端到端跑通**——真实取证数据 → JSON → 关系图，工具链闭环。

**暴露的 1 个实质问题（Phase 5 层面的）**：
- **rxs-cc-plugins 与 memory 中"Phase 5 = rxs API 层命名空间改造"对不上**。此仓库无 rxs::、无 API 层、C++17——Phase 5 的真正目标是 rxs-toolkit/rxs-algorithms（有 rxs_export.h/rxs_api.h 的仓库），rxs-cc-plugins 是**下游工具集，尚未对齐 rxs::**。
- **对锐哥的启示**：① Phase 5 落地前需确认"目标仓库边界"（哪些仓库含 API 层、哪些只需下游对齐）；② G3 验收门"下游按 rxs::measure:: 对齐"在当前 rxs-cc-plugins 上**不成立**（它无 rxs:: 引用，对齐对象应为 rxs-toolkit 体系的仓库）。

## 八、下一步建议

1. **你来裁决 G3**：rxs-cc-plugins 是否属 rxs:: 改造目标？arsenal/czxEigen 是否计划并入 rxs::？
2. **clone rxs-toolkit / rxs-algorithms 补跑**（Phase 5 真正目标）：验证 rxs_export.h/rxs_api.h 的 API 层改造沉淀——那才是"不可逆抉择"（导出宏形态、命名空间、C++ 标准）的实战场。
3. 本实测的 prd.json 已存 `docs/phase5-factcheck.json`，可作 grill-to-PRD 的第二个自测样例（真实代码版）。

---

## 九、裁决修正与新增发现（2026-08-25 用户改口）

**修正**：用户裁决修正——**rxs-cc-plugins 属 rxs:: 改造目标**（原判"非目标"被改口）。G3 验收门状态从"待决"变"已裁决：是"。
这个改口本身是治理规范"用户改主目标才可回退"的实例——**不可逆抉择的裁决权在用户，且裁决可修正**（B1 主目标可被用户显式指令改写）。

**新增发现（E1，rxs-toolkit/czxDependence grep）**：**czxDependence 是跨仓库共享工具库**——rxs-toolkit 与 rxs-cc-plugins 各带一份副本，**均为 arsenal/czxEigen 命名空间**。rxs-toolkit 自身也是"双轨"：公共 API 层已 rxs::，内部工具库仍 arsenal/czxEigen。

**由此产生的新不可逆抉择（建议 ADR）**：**rxs:: 化边界到哪一层？**
- 方案 A：仅公共接口 rxs::，内部工具库保持 arsenal/czxEigen（= 当前 rxs-toolkit 状态，工程量最小）
- 方案 B：全库 rxs::（含 czxDependence）——工程量最大，且 czxDependence 跨仓库共享，**两仓库必须同步改造防分叉**
- 方案 C：中间态——rxs-cc-plugins 公共接口 rxs::，工具库保留（对齐 rxs-toolkit 双轨模式）

三方案均满足 ADR 三触发条件（难逆转/无上下文惊讶/真实取舍），**这是 Phase 5 当前最需要用户裁决的不可逆抉择**。

---

*标签：全部取证 E1（grep 真代码）；假设对账 E2（memory 记录 vs 真代码）；G3 已用户裁决 E3（2026-08-25 修正）。*
