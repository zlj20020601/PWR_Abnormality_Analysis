# PWR_Abnormality_Project

## 1. 项目概述
本项目针对 **PWR（压水堆）多传感器运行数据**，构建了一套 **无监督异常检测与关键变量排查** 流程。

项目目标不是直接给出“故障类别标签”，而是：
1. 在**无标签**条件下识别异常候选样本；
2. 定位异常窗口；
3. 通过特征分析、变量排查、方法对比和参数稳健性分析，验证异常窗口是否可信。

---

## 2. 为什么使用无监督学习
原始数据集中没有明确的 `label / target / class` 列，因此无法直接进行监督分类。

因此本项目先采用无监督异常检测方法：
- **Isolation Forest**：作为 baseline
- **LOF（Local Outlier Factor）**：作为对比验证方法

无监督方法的作用是：
- 先从多变量分布中找到“和大多数样本不一样的区域”
- 再结合物理量和特征分析，判断这些异常候选是否可信

---

## 3. 数据说明
原始数据文件：
- `data/PWR Abnormality Dataset.csv`

数据基本情况：
- 样本数：**12267**
- 原始列数：**17**
- 建模特征数：**16**（删除 `Readings` 后）

主要变量包括：
- 温度：`Temperature`
- 压力：`Pressure`
- 流量：`Flow1`, `Flow2`
- 传感器变量：`VRR12`, `VRR22`, `VRR23`, `VRR33`, `VRS01`, `VRS03`, `VRS21`, `VRS31`, `VRS02`, `VRI01`, `VRI02`, `VRI03`

---

## 4. 数据预处理
本项目完成了以下清洗与预处理步骤：

1. 检查缺失值与重复值  
   - 原始数据无缺失、无重复

2. 修复 `Flow2` 格式问题  
   - 发现个别值使用逗号小数格式，例如 `13077,1`
   - 统一转为标准数值格式

3. 删除 `Readings`  
   - `Readings` 仅作为编号列，不参与建模

4. 标准化  
   - 使用 `StandardScaler`
   - 解决不同变量量纲差异问题

---

## 5. 方法流程
本项目主线流程如下：

1. 数据检查与清洗  
2. Isolation Forest baseline  
3. 异常分数全局/局部分析  
4. 异常窗口特征分析  
5. `VRR12` 可疑变量专项排查  
6. 去掉 `VRR12` 的消融实验  
7. LOF 方法复核  
8. contamination 参数敏感性分析

---

## 6. 项目结构
```text
PWR_Abnormality_Project/
├── data/
│   └── PWR Abnormality Dataset.csv
├── notebooks/
│   ├── 01_data_check.ipynb
│   ├── 02_baseline_isolation_forest.ipynb
│   ├── 03_feature_analysis.ipynb
│   ├── 04_vrr12_investigation.ipynb
│   ├── 05_without_VRR12.ipynb
│   ├── 06_lof_validation.ipynb
│   └── 07_contamination_sensitivity.ipynb
├── outputs/
│   ├── figures/
│   └── tables/
├── src/
│   ├── data_utils.py
│   ├── model_utils.py
│   └── plot_utils.py
├── main.py
└── README.md
```

---

## 7. 各 notebook 的作用
### 01_data_check.ipynb
完成数据基础检查：
- 列名、数据类型
- 缺失值/重复值
- `Flow2` 格式异常定位
- `Readings` 是否为编号列确认

### 02_baseline_isolation_forest.ipynb
完成 baseline：
- 标准化
- Isolation Forest
- 异常标签与异常分数
- 异常分数全局图与局部图
- 温度-压力散点图
- top10 最异常样本

### 03_feature_analysis.ipynb
围绕主异常窗口 `12115~12135` 做特征解释：
- 均值差异
- mean/std/median/IQR/effect size
- 温度、压力、Flow2 等局部图
- 发现 `VRR12` 差异异常强

### 04_vrr12_investigation.ipynb
单独排查 `VRR12`：
- 全局曲线
- 描述统计
- 平台切换
- 是否接近 100 倍量级变化

### 05_without_VRR12.ipynb
消融实验：
- 去掉 `VRR12` 后重跑 Isolation Forest
- 验证主异常窗口是否仍存在

### 06_lof_validation.ipynb
使用 LOF 进行第二方法验证：
- 比较主异常窗口是否仍然出现
- 识别局部孤立点异常

### 07_contamination_sensitivity.ipynb
参数稳健性分析：
- 比较 contamination = 0.01 / 0.03 / 0.05 / 0.08 / 0.10
- 检查主异常窗口是否稳定存在

---

## 8. 核心发现
### 8.1 主异常窗口
Isolation Forest baseline 在末端识别出一个明显连续异常窗口：
- **主异常窗口：12115 ~ 12135**

该窗口在：
- 异常分数局部图中呈现明显低谷
- top10 最异常样本中高度集中
- 不同 contamination 下保持稳定
- 去掉 `VRR12` 后依然存在
- LOF 也对该区段给出支持

### 8.2 两类异常模式
当前结果显示，数据中至少存在两类异常模式：

1. **连续窗口异常**  
   - 代表区间：`12115 ~ 12135`
   - 特征：高温高压平台后段内的连续异常区段

2. **孤立点异常**  
   - 代表点：`5336`
   - 特征：低温低压主导的单点极端异常

### 8.3 VRR12 的角色
`VRR12` 在异常窗口内出现显著量级切换：
- 大部分区间约为 `19.06`
- 异常窗口附近约为 `0.19`

这说明：
- `VRR12` 不像普通噪声
- 更像背景状态切换、缩放/量纲变化，或可疑传感器变量

但消融实验表明：
- **去掉 `VRR12` 后，主异常窗口仍然存在**
- 因此主异常窗口并非由 `VRR12` 单独驱动，而是由温度、压力、Flow2 等多变量共同支撑

---

## 9. 结果为什么可信
本项目并不是只跑了一个模型就下结论，而是通过多种方式做了交叉验证：

1. **多图证据**
   - 异常分数全局图
   - 异常分数局部图
   - 温度/压力局部图
   - 温度-压力散点图

2. **特征分析**
   - 均值差异
   - 标准差
   - 中位数
   - IQR
   - effect size

3. **变量排查**
   - `VRR12` 单独调查
   - 缩放/量级切换验证

4. **消融实验**
   - 去掉 `VRR12` 后重跑模型

5. **方法对比**
   - Isolation Forest
   - LOF

6. **参数稳健性分析**
   - 不同 contamination 下主异常窗口持续存在

因此，本项目结论不是“单一步骤得出的偶然结果”，而是多证据链共同支持的结果。

---

## 10. 如何复现
### 运行顺序建议
按以下顺序运行 notebook：

1. `01_data_check.ipynb`
2. `02_baseline_isolation_forest.ipynb`
3. `03_feature_analysis.ipynb`
4. `04_vrr12_investigation.ipynb`
5. `05_without_VRR12.ipynb`
6. `06_lof_validation.ipynb`
7. `07_contamination_sensitivity.ipynb`

### 环境建议
建议使用：
- Python 3.10
- pandas
- matplotlib
- scikit-learn

### 安装依赖
```bash
pip install pandas matplotlib scikit-learn jupyter
```

---

## 11. 当前阶段结论
本项目当前已经完成一个**可复现、可解释、可用于简历与面试表达的无监督异常检测主线版本**。

最终阶段性结论为：
- 数据中存在稳定的主异常窗口 `12115~12135`
- 该窗口对应高温高压平台后段的连续异常区段
- `VRR12` 是可疑背景变量，但并不单独决定主异常窗口
- 主异常窗口在模型、参数和变量消融层面均表现出较好的稳健性
