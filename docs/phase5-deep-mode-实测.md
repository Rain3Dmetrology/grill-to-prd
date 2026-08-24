# grill-to-PRD Deep 模式实测：Phase 5 rxs API 层命名空间改造

**实测目的**：验证 v0.1.0 的 Deep 模式是否真能对真实需求沉淀「领域名词关系图 + 不可逆抉择 + 验收门」。
**输入**：Phase 5 真实需求（来源：项目记忆，本机无 rxs 代码，故 fact 项标注为 [待 E1 取证]）。
**方法**：严格按 SKILL.md 的 grilling 设计树 + frontier 分轮执行。
**日期**：2026-08-25

---

## 第 0 步：B1 主目标冻结

| 字段 | 值 |
|---|---|
| **目的（用户原话）** | rxs API 层命名空间改造：rxs_export.h 重写 + rxs_api.h 接口层 + rxs_api.cpp 实现 + CMakeLists.txt 更新 |
| **IN scope** | 4 个文件 + 命名空间重命名 |
| **OUT of scope** | 算法实现、GUI、其他仓库（qmacvisual 仅对齐命名空间约定） |

## 第 1 轮 frontier 拷问（设计树第一层）

> 按 grilling 规则：**fact 归 agent（本机无代码→标待取证），decision 归用户（不可逆抉择逐项确认）**。

| # | frontier 问题 | 类型 | 现状 |
|---|---|---|---|
| Q1 | 命名空间最终形态：全局 `rxs::` vs `rxs::measure::`（qmacvisual 子空间） | **decision（不可逆）** | memory 记录"统一 rxs::，qmacvisual 用 rxs::measure::"——需用户确认这是否仍是最终决定 |
| Q2 | 是否保留 `vision3d::` 别名做向后兼容？ | decision | 未知，需问 |
| Q3 | 导出宏命名：`RXS_EXPORT` vs `RXS_API` vs 沿用旧名 | decision | 未知，需问 |
| Q4 | C++ 标准基线：C++20（C++17 最低兼容）？ | **decision（不可逆）** | memory 记录"C++20 基线，C++17 最低兼容" |
| Q5 | `std::expected` 方案：C++20 下用 `tl::expected` vs 直接升 C++23 | **decision（不可逆）** | memory 记录"C++23 的 std::expected，C++20 用 tl::expected" |

**fact 项（agent 应自己取证，不归用户）**：PCL/CGAL/OCCT/OpenCV 的实际版本兼容性、现有代码里 `vision3d::` 的出现次数（决定 Q2 的工作量）——**本机无代码，标 [待 E1 取证]**。

## 领域名词关系图（graph 派生，`scripts/graph_derive.py` 思想）

```
graph LR
    rxs命名空间 -->|depends_on| C++20基线
    rxs命名空间 -->|depends_on| 导出宏形态
    rxs命名空间 -.->|constrained_by| vision3d向后兼容
    C++20基线 -.->|constrained_by| PCL/CGAL/OCCT/OpenCV版本
    C++20基线 ==>|locked_by| G1
    tl::expected -.->|constrained_by| C++20基线
    tl::expected ==>|locked_by| G2
    qmacvisual_rxs_measure ==>|locked_by| G3
```

## 不可逆抉择 ADR（domain-modeling 三触发条件全满足才写）

### ADR-0001：命名空间统一为 `rxs::`
- **难逆转** ✅：一旦落地，所有引用点（跨 6+1 仓库）都要改，改口成本极高
- **无上下文会惊讶** ✅：后人会问"为什么叫 rxs 而不是 vision3d"
- **真实取舍** ✅：`vision3d::`（历史名，语义窄）vs `rxs::`（品牌名，覆盖全部产品线）——选了后者
- **状态**：✅ 三条件满足，必须写 ADR

### ADR-0002：C++20 基线 + tl::expected（不升 C++23）
- **难逆转** ✅：ABI/编译标准锁定
- **真实取舍** ✅：C++23 的 `std::expected` vs C++20 的 `tl::expected`（依赖 tl 库）
- **状态**：✅ 必须写 ADR

## 验收门 G1-G3（验收命令先行）

| 门 | 定义 | 验收命令 | 证据 |
|---|---|---|---|
| G1 单元 | 命名空间重命名后单文件编译通过 | `cmake --build . --target rxs_api` 无 vision3d 残留 | E1 |
| G2 集成 | 全仓库链接通过 + 无 `vision3d::` 残留 | `grep -r "vision3d::" .` 返回空 + 全量编译 | E2 |
| G3 实机 | qmacvisual 等下游仓库按 `rxs::measure::` 对齐 | 下游仓库编译 + 用户确认 | E3 |

---

## 实测结论（刻薄自评）

**验证通过的**：grill-to-PRD 的 Deep 模式**确实能把 Phase 5 的领域名词（rxs::/vision3d::/tl::expected/C++20 基线/导出宏）组织成三类资产**——关系图（graph 派生）、不可逆抉择 ADR（三触发条件判据）、验收门 G1-G3（验收命令先行）。这是 v0.1.0 最该验证的核心能力，**框架成立**。

**暴露的 3 个真实缺口（诚实披露）**：
1. **fact 取证依赖代码在盘**：Q1/Q2 的"不可逆抉择"要用户确认，但 Q2 的决策（vision3d 别名兼容）其实**取决于代码里 `vision3d::` 出现次数**——代码不在本机，skill 只能标 [待 E1 取证] 而非真查。这印证了 grilling 的"fact 归 agent"机制是对的，但**实测环境缺了 fact 源**。
2. **ADR 三触发条件是"判据"不是"自动写"**：skill 只能"提示该写 ADR"，真正写 ADR 还是 agent 执行——三触发条件减低了"过度写 ADR"的风险（正是你要的"避免过度约束"），但需实测多轮才知松紧。
3. **graph 派生目前只覆盖"已知关系"**：本机无代码，无法验证"从代码自动抽取术语关系"（那需要 R13 的代码库取证）。当前 graph 是"人工确认的关系"，非"自动发现的隐藏关系"。

**一句话**：Deep 模式的**框架验证通过**（能沉淀关系图 + 不可逆抉择 + 验收门），但**端到端价值仍需一次"有代码在盘"的真跑**——建议下次在 rxs 项目所在机器（或 clone 仓库后）补跑，重点验 Q2 的 fact 取证闭环。

---

*标签：本实测基于 memory 真实信息 [KNOWN]，fact 项因无代码标 [待 E1 取证]，ADR 三触发判据与验收门为 [COMPUTED]。*
