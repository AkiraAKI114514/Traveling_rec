# Traveling_rec - 基于专家系统的智能旅游推荐引擎

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

`Traveling_rec` 是一个融合了 **逻辑推理引擎 (Inference Engine)** 与 **动态规划 (Dynamic Programming)** 算法的现代化旅游推荐系统。与传统的简单搜索不同，本项目模拟旅游专家的决策过程，通过预设规则和属性推导，为用户在预算范围内匹配最优的旅行方案。

---

##  核心特性

* ** 专家系统推理机**：核心模块 `Logic_engine.py` 采用前向推理算法，结合 `rules.py` 中的规则库，实现从“用户兴趣”到“具体属性”的逻辑推导。
* ** 动态规划决策**：利用 `DPReasoning.py` 中的背包算法（Knapsack Algorithm）思想，在用户设定的预算（Budget）限制下，计算得分最高的景点组合。
* ** 实时数据采集**：集成 Selenium 自动化工具 (`findattri.py`)，支持从旅游平台实时获取最新的景点评分、价格和标签。
* ** 自动化数据维护**：支持通过 `Sql_updating.py` 自动清洗和更新本地 SQLite 数据库，确保推荐信息的时效性。

---

##  项目结构

```text
Traveling_rec/
├── main.py              # 程序入口：负责用户交互逻辑
├── Logic_engine.py      # 逻辑引擎：核心前向推理模块
├── DPReasoning.py       # 推理算法：执行基于预算的动态规划选择
├── rules.py             # 规则库：定义专家系统的判定逻辑
├── findattri.py         # 爬虫模块：基于 Selenium 的数据采集工具
├── Sql_updating.py      # 数据库维护：管理 travel.db 的更新与同步
├── repair.py            # 修复工具：数据库完整性校验与修复
├── travel.db            # 核心数据库：存储景点、城市及逻辑规则
└── Requirements.txt     # 项目依赖清单
```
# 克隆仓库
git clone [https://github.com/AkiraAKI114514/Traveling_rec.git](https://github.com/AkiraAKI114514/Traveling_rec.git)
cd Traveling_rec

# 安装必要依赖
pip install -r Requirements.txt

# Run code:
python main.py
