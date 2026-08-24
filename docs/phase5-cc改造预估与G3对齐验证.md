# Phase 5 补全：rxs-cc-plugins 改造预估 + G3 下游对齐验证

**日期**：2026-08-25　**裁决**：方案 C（公共接口 rxs:: + 工具库 arsenal/czxEigen 保留）
**代码源**：rxs-cc-plugins / rxs-algorithms（已 clone）

---

## 一、rxs-cc-plugins 命名空间重命名影响面分析（方案 C）

### 1.1 取证事实（E1）

| # | 事实 | 证据 |
|---|---|---|
| F1 | arsenal/czxEigen **只存在于 czxDependence 工具库内部**（两个副本：根目录 + mesh2cad/） | grep：仅 czxTool.cpp/czxTool.h |
| F2 | **主代码（delaunay/pcd2stl/meshSlice 源.cpp）零引用 arsenal/czxEigen** | grep 排除 czxDependence 后为空 |
| F3 | 主代码无显式命名空间（全局作用域） | pcd2stl.h 类 `pcd2stl` 无 namespace 包裹 |
| F4 | 主代码无 DLL 导出宏（静态工具形态） | grep RXS_EXPORT/__declspec = 0 |
| F5 | 项目名已带 rxs 前缀（rxs_cc_plugins / rxs_mesh2cad） | CMakeLists project() |

### 1.2 方案 C 改造预估（最小侵入）

| 项 | 动作 | 影响面 | 预估 |
|---|---|---|---|
| 主代码命名空间化 | pcd2stl / delaunay / meshSlice 源.cpp 包入 `namespace rxs::cc`（或 rxs::tools） | 约 5-8 个文件（每个 +2 行包裹 + 引用处限定） | **1-2 小时级** |
| czxDependence | **零改动**（保留 arsenal/czxEigen） | 0 | 防跨仓库分叉 |
| 头文件 include 路径 | `../czxDependence/czxTool.h` 相对路径（可留或规范化） | 低 | 可选 |
| 消费者同步 | 调用 pcd2stl/delaunay 的下游（如 qmacvisual）须加 rxs::cc:: 限定 | 待查下游 | 待查 |
| DLL 导出 | 当前无需（静态工具）；若未来 DLL 化再加 rxs_export.h | — | 不纳入本次 |

**核心结论**：方案 C 在 rxs-cc-plugins 上的改造**比想象小一个数量级**——主代码本就不引用 arsenal/czxEigen（只是没命名空间），实质是"加命名空间包裹"，而非"重命名引用"。**真正的架构约束在 czxDependence 共享工具库**（保留即防分叉，但意味着两仓库长期双轨）。

## 二、G3 下游对齐验证（rxs-algorithms）

### 2.1 取证事实（E1）

| 仓库 | 命名空间 | 判定 |
|---|---|---|
| rxs-toolkit | 公共 API 层 `rxs::` ✅；工具库 czxDependence 仍 arsenal/czxEigen（双轨） | **部分对齐** |
| rxs-algorithms | **module 层全部 `namespace rxs`**（flatness/ellipse_fitting/linear_regression/coplanarity 等） | **✅ 已对齐** |
| rxs-cc-plugins | arsenal/czxEigen（工具库）+ 全局命名空间（主代码） | ❌ 待改造（方案 C） |
| rxs-qmacvisual | 未验证（memory 记 rxs::measure::） | 待查 |

### 2.2 结论

**G3 下游对齐状态：rxs-algorithms ✅ 已对齐 rxs::**，rxs-cc-plugins 按方案 C 改造后达标，rxs-qmacvisual 待补验。
**rxs-algorithms 细节**：vcpkg.json 依赖管理（OCCT 等），CMakePresets——是独立 module 化架构，`namespace rxs` 在其 module 层已成标准。

---

*标签：全部取证 E1（grep/read 真代码）；改造预估为 [COMPUTED]（基于影响面）；qmacvisual 未验证 [UNVERIFIED]。*
