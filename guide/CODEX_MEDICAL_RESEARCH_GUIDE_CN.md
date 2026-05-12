# 用 Codex 跑一次孟德尔分析

你现在手里有两份 GWAS 数据：

```text
data/exposure_bmi.csv
data/outcome_chd.csv
```

我们不讲太多概念，直接开始。目标很明确：

> 用 BMI 作为暴露，冠心病作为结局，跑一次两样本孟德尔分析，并把代码、结果表、图片都整理好。

你只需要把数据放进项目文件夹，然后把下面的任务交给 Codex。

## 第一步：让 Codex 先看数据

先不要急着跑分析。你可以这样对 Codex 说：

```text
我已经把两份 GWAS 数据放在 data/ 文件夹：
1. data/exposure_bmi.csv
2. data/outcome_chd.csv

请先检查这两个文件：
1. 行数和列数。
2. 列名。
3. 每列缺失值。
4. SNP 是否重复。
5. beta、se、pval 是否为数值。
6. 暴露数据中 p < 5e-8 的 SNP 数量。

请把检查代码保存为 scripts/01_check_data.R。
请把检查结果保存为 results/data_check_report.csv。
```

Codex 会先写一个检查脚本，然后运行它。你会看到类似这样的结果：

```text
exposure_bmi.csv: 2,350,418 行，8 列
outcome_chd.csv: 1,820,774 行，8 列

必要字段检查：通过
重复 SNP 检查：暴露数据 0 个，结局数据 0 个
缺失值检查：通过
p < 5e-8 的 BMI 工具 SNP：312 个
```

这一步很重要。  
你不用自己打开 Excel 一列列看，Codex 会帮你先确认数据能不能进入下一步。

## 第二步：让 Codex 写孟德尔分析代码

数据检查通过后，你继续说：

```text
请根据刚才的数据检查结果，写 R 脚本完成两样本孟德尔分析。

要求：
1. 使用 TwoSampleMR。
2. 读取 data/exposure_bmi.csv 和 data/outcome_chd.csv。
3. 筛选暴露数据中 p < 5e-8 的 SNP。
4. 计算每个 SNP 的 F statistic。
5. 做 LD clumping。
6. harmonise 暴露和结局数据。
7. 运行 IVW、MR-Egger、weighted median、weighted mode。
8. 输出 OR、95%CI、P 值。
9. 做异质性检验。
10. 做 MR-Egger 截距检验。
11. 做 leave-one-out 分析。

请把脚本保存为 scripts/02_run_mendelian_analysis.R。
请把所有结果表保存到 results/。
如果运行报错，请直接根据报错修改代码。
```

Codex 会生成并运行脚本。跑完后，项目里会多出这些文件：

```text
results/
  instrument_variables.csv
  harmonised_data.csv
  mr_results.csv
  heterogeneity.csv
  pleiotropy.csv
  leave_one_out.csv
```

你可以让 Codex 打开 `mr_results.csv`，它会把结果整理成这样：

| 方法 | OR | 95%CI | P 值 |
|---|---:|---:|---:|
| IVW | 1.30 | 1.15-1.48 | <0.001 |
| MR-Egger | 1.22 | 0.98-1.52 | 0.072 |
| Weighted median | 1.27 | 1.10-1.46 | 0.001 |
| Weighted mode | 1.24 | 1.03-1.49 | 0.024 |

你不需要手动复制结果。  
你可以继续问：

```text
请把 results/mr_results.csv 整理成适合放进文章的中文结果描述。
```

Codex 可以给你这样的摘要：

```text
IVW 分析显示，BMI 升高与冠心病风险增加相关
（OR=1.30，95%CI：1.15-1.48，P<0.001）。
Weighted median 和 weighted mode 结果方向一致。
MR-Egger 结果方向一致，但未达到统计学显著。
```

## 第三步：让 Codex 生成图

结果有了，接下来让 Codex 画图：

```text
请根据 results/ 中的孟德尔分析结果生成图。

要求：
1. 散点图。
2. 森林图。
3. 漏斗图。
4. leave-one-out 图。

请把绘图代码保存为 scripts/03_make_plots.R。
请把图片保存到 figures/，同时保存 PDF 和 PNG 两种格式。
```

跑完后，你会得到：

```text
figures/
  scatter_plot.pdf
  scatter_plot.png
  forest_plot.pdf
  forest_plot.png
  funnel_plot.pdf
  funnel_plot.png
  leave_one_out.pdf
  leave_one_out.png
```

这时候你已经有了：

- 检查脚本
- 分析脚本
- 绘图脚本
- 结果表
- 图片
- 初步结果描述

这就是一次完整的孟德尔分析工作流。

## 如果中途报错，就让 Codex 接着修

比如你运行时遇到这个报错：

```text
Error: None of the specified columns are present
```

你不用自己猜。直接告诉 Codex：

```text
运行 scripts/02_run_mendelian_analysis.R 时报错：
Error: None of the specified columns are present

这是 exposure_bmi.csv 的列名：
rsid, ea, nea, b, standard_error, p_value, eaf, n

这是 outcome_chd.csv 的列名：
SNP, effect_allele, other_allele, beta, se, pval, eaf, samplesize

请修改脚本，让它能识别这两种列名格式。
```

Codex 会改代码，把列名映射成统一格式：

```text
rsid -> SNP
ea -> effect_allele
nea -> other_allele
b -> beta
standard_error -> se
p_value -> pval
n -> samplesize
```

然后它会重新运行脚本。  
这就是 Codex 和普通教程最大的区别：教程只能告诉你“应该怎么做”，Codex 可以根据你真实的报错继续改。

## 最后让 Codex 整理项目

分析跑完后，你可以让 Codex 收尾：

```text
请整理整个孟德尔分析项目。

要求：
1. 确认 data/、scripts/、results/、figures/ 是否完整。
2. 生成 README.md。
3. README 中说明每个脚本的作用。
4. README 中说明如何从原始数据复现结果。
5. README 中列出最终输出文件。
```

最后，你的项目会像这样：

```text
mendelian_bmi_chd/
  data/
    exposure_bmi.csv
    outcome_chd.csv
  scripts/
    01_check_data.R
    02_run_mendelian_analysis.R
    03_make_plots.R
  results/
    data_check_report.csv
    instrument_variables.csv
    harmonised_data.csv
    mr_results.csv
    heterogeneity.csv
    pleiotropy.csv
    leave_one_out.csv
  figures/
    scatter_plot.pdf
    forest_plot.pdf
    funnel_plot.pdf
    leave_one_out.pdf
  README.md
```

你再回头看，会发现 Codex 帮你做的不是一句“AI 回答”，而是一整套分析工程：

- 它读了数据。
- 它写了代码。
- 它跑了分析。
- 它修了报错。
- 它导出了结果。
- 它画了图。
- 它整理了项目。

## 你可以直接复制的完整提示词

如果你只想快速开始，把下面这一段直接发给 Codex：

```text
我已经有两份 GWAS 数据：
data/exposure_bmi.csv
data/outcome_chd.csv

请帮我完成一次两样本孟德尔分析，使用 BMI 作为暴露，冠心病作为结局。

请按下面流程执行：
1. 检查两个 CSV 文件的行数、列名、缺失值、重复 SNP、数值列类型。
2. 输出 results/data_check_report.csv。
3. 使用 TwoSampleMR 写 R 分析脚本。
4. 筛选 p < 5e-8 的工具 SNP。
5. 计算 F statistic。
6. 做 LD clumping。
7. harmonise 暴露和结局数据。
8. 运行 IVW、MR-Egger、weighted median、weighted mode。
9. 输出 OR、95%CI、P 值。
10. 做异质性检验、MR-Egger 截距检验、leave-one-out 分析。
11. 保存所有结果到 results/。
12. 生成散点图、森林图、漏斗图、leave-one-out 图，保存到 figures/。
13. 代码保存到 scripts/。
14. 如果报错，请根据报错继续修改并重新运行。
15. 最后生成 README.md，说明如何复现分析。
```

现在你可以打开 Codex，把数据放好，然后让它开始跑。  
你不需要一开始就懂全部代码；你只需要把任务说清楚，让 Codex 一步步把孟德尔分析做出来。
