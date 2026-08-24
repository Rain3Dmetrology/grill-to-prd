# grill-to-PRD Deep 实测：rxs-toolkit（Phase 5 真正目标仓库）

**实测目的**：对 Phase 5 真正目标仓库做有代码在盘取证，验证领域名词关系图 + 不可逆抉择 ADR + 验收门沉淀，并对账 memory 假设。
**代码源**：`https://github.com/rxsvision/rxs-toolkit.git`（已 clone 至 D:\Downloads\rxs-toolkit）
**工具链**：grep/Read 取证（E1）+ `scripts/graph_derive.py` + ADR 三触发判据
**日期**：2026-08-25

---

## 一、取证结果（全部 E1：真代码）

| # | 取证项 | 证据 | 结果 |
|---|---|---|---|
| F1 | API 层存在性 | include/rxs/rxs_export.h + rxs_api.h + src/rxs_api.cpp | **Phase 5 三件套齐备**（2026-06-29 注释日期） |
| F2 | 命名空间 | rxs_api.h:45 `namespace rxs` | **rxs:: 已落地** |
| F3 | vision3d:: 残留 | grep 全仓库 | **0 处** |
| F4 | C++ 标准 | CMakeLists.txt:15 | **C++17**（非 memory 假设的 C++20） |
| F5 | PCL 版本 | CMakeLists.txt:22 | **PCL 1.10**（非 memory 假设的 1.15.1-rc1） |
| F6 | 导出宏 | rxs_export.h | **RXS_API 三态**（静态=空/导出=dllexport/导入=dllimport）+ RXS_LOCAL |
| F7 | API 数量 | rxs_api.h | 18 个算法 API + ToolkitHandle（动态加载兼容层） |
| F8 | DLL 输出名 | CMakeLists.txt:100 | **仍为 czxToolkit**（OUTPUT_NAME），Source.def 定义 18 导出 |
| F9 | 头文件安装 | CMakeLists.txt:199-207 | 双轨：新 API → include/rxs，旧头 → include/rxs-toolkit |

## 二、假设 vs 现实对账（memory vs 真代码）

| memory 假设 | rxs-toolkit 真代码 | 判定 |
|---|---|---|
| Phase 5 中断待恢复 | **rxs_api.h/rxs_api.cpp 已存在且完整**（18 API + ToolkitHandle） | **假设过时**——Phase 5 主体已完成 |
| 命名空间统一 rxs::（曾 vision3d::） | rxs:: 已落地，vision3d:: 残留 0 | 假设方向对，状态已推进 |
| C++20 基线 | **C++17** | 假设有误（两个仓库均 C++17） |
| PCL 1.15.1-rc1 | **PCL 1.10** | 假设有误 |
| — | DLL 名保留 czxToolkit + Source.def | 新增事实：向后兼容设计 |

> **实测核心价值**：若按 memory 假设重启"Phase 5 改造"，会**重做已完成的工作**（rxs:: 已落地）+ **基于错误基线**（C++20/PCL 1.15）改配置。有代码在盘取证直接阻止了这场返工。

## 三、真实领域名词（rxs-toolkit，已落地体系）

`rxs`（命名空间）· `RXS_API`/`RXS_LOCAL`（导出宏三态）· `PointT`/`CloudT`/`CloudPtr` · `BaseFace`/`FlatnessResult`/`KeyboardResult` · `LaptopType`/`PhotometricMode`（枚举）· `fitBSpline`/`semiconductor`/`keyboard`/`registration`/`computeConvexHull`/`laptopCalculation`/`photometricStero` 等 18 API · `ToolkitHandle`（动态加载）· `czxToolkit.dll` · `Source.def` · PCL/OpenCV/Eigen/FLANN/Boost/OpenMP

## 四、不可逆抉择 ADR（三触发条件判据，真实评估）

### ADR-0001：namespace rxs 现代 API 层（已完成 ✅）
- **难逆转** ✅：18 API 签名 + 下游引用一旦落地，改口成本高
- **无上下文惊讶** ✅：后人会问"为什么 rxs:: 包着 czxToolkit"
- **真实取舍** ✅：类型安全 API + ToolkitHandle 动态加载 vs 裸 GetProcAddress——选了前者（双轨兼容）
- **状态**：**已落地，无需新写**——skill 的 ADR 判据在此正确识别"决策已发生"

### ADR-0002：DLL 输出名保留 czxToolkit（向后兼容）
- **难逆转** ✅：改名 = 下游 6+1 仓库全部改链接
- **真实取舍** ✅：改名 rxs-toolkit.dll（语义新）vs 保留 czxToolkit.dll（兼容旧消费者）——选了后者
- **状态**：**已决策**，Source.def 为证据

### 候选 ADR（待用户裁决，证据已足）：
- **C++17 → C++20 是否升级？**（memory 期望 C++20，真代码 C++17）——三触发条件全满足（改口成本高/无上下文惊讶/真实取舍），**这是当前最有价值的待决不可逆抉择**

## 五、关系图（`graph_derive.py` 派生思想）

```
graph LR
    rxs_api层 -->|depends_on| rxs命名空间
    rxs_api层 -->|depends_on| RXS_API导出宏
    rxs_api层 -->|depends_on| czxToolkit.dll
    RXS_API导出宏 -.->|constrained_by| C++17标准
    rxs_api层 -.->|constrained_by| PCL_1.10
    czxToolkit.dll ==>|locked_by| Source.def_18导出
    C++17标准 ==>|locked_by| G2_编译验收
    rxs_api层 ==>|locked_by| G3_下游对齐
```

## 六、验收门（真实，当前状态）

| 门 | 定义 | 验收命令 | 证据 | 状态 |
|---|---|---|---|---|
| G1 单元 | rxs_api.h 头编译 | 单文件编译含 rxs/rxs_api.h | E1 | 待跑（需 VS+PCL） |
| G2 集成 | 全库编译 + 无残留 | `cmake --build` + grep vision3d=0 | E2 | **vision3d=0 已验**；编译待跑 |
| G3 实机 | 下游仓库用 rxs:: API 对齐 | rxs-algorithms/qmacvisual 编译 + 用户确认 | E3 | 待跑 |

## 七、实测结论

**验证通过的**：grill-to-PRD 对**真正目标仓库**完成了全量取证，识别出：
1. **Phase 5 实际状态 ≠ memory 假设**（已完成 vs 中断）——避免了重启已完成工作的返工；
2. **两个已落地 ADR**（rxs:: API 层、czxToolkit DLL 名保留）+ **一个待决不可逆抉择**（C++17→C++20 升级）——ADR 判据精准区分"已决策/待决策"；
3. **验收门 G2 已部分实证**（vision3d 残留=0 真跑）。

**暴露的 2 个 skill 层面缺口（诚实披露）**：
1. **"决策已发生"的识别**：skill 能取证（rxs:: 已落地），但判断"这是已完成的历史决策还是待做的新决策"需要结合仓库 git 历史/提交时间——建议 Deep 模式增加"提交历史取证"（git log 该文件，确认决策时间点）。
2. **多仓库对账场景**：rxs-toolkit（rxs::）vs rxs-cc-plugins（arsenal/czxEigen）命名空间不一致——这正是"下游对齐"验收门的来源，但需要用户显式声明仓库边界（本实测已获裁决：rxs-cc-plugins 非目标）。

**一句话**：**Phase 5 的实战场取证完成——主体已落地，剩余真正待决项是 C++ 标准升级（C++17→C++20）+ 下游对齐验证**，而不是 memory 假设的"重启改造"。

## 八、下一步建议

1. **你来裁决候选 ADR**：C++17 → C++20 是否升级？（影响：CMakeLists 一行 + 依赖库版本要求）
2. **补跑编译验收**：本机有 VS2022 后跑 `cmake --build`（G2），验证 rxs_api 层可编译——这是 G1/G2 验收命令的真执行。
3. 若需继续，可 clone rxs-algorithms / rxs-qmacvisual 补跑 G3 下游对齐验证。

---

*标签：全部取证 E1（grep/read 真代码）；对账 E2；待决项 G3/候选 ADR 待用户裁决 E3。*
