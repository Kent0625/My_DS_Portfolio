# From Farm to Cup

**Statistical Case Study: Bootstrap & BCa Confidence Intervals for Coffee Farmer Income Uncertainty**

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)](https://github.com/Kent0625/bootstrap-coffee-farmers-income)
[![Language](https://img.shields.io/badge/Language-R-276DC3?style=flat-square&logo=r)](https://www.r-project.org/)
[![Method](https://img.shields.io/badge/Method-BCa_Bootstrap-orange?style=flat-square)](https://github.com/Kent0625/bootstrap-coffee-farmers-income)

A statistical case study using non-parametric bootstrap resampling and Bias-Corrected and Accelerated (BCa) confidence intervals to examine coffee farmer income uncertainty in Bukidnon, Philippines.

---

## Key Metrics at a Glance

| Metric / Attribute | Value / Specification |
| :--- | :--- |
| **Dataset Size** | 200 coffee farmer records (Bukidnon, Northern Mindanao) |
| **Statistical Framework** | Non-parametric Bootstrap Resampling ($B = 2,000$) |
| **Confidence Method** | Bias-Corrected and Accelerated (BCa) & Percentile Intervals |
| **Analysis Stack** | R, `boot` library, `ggplot2` |
| **Source Code** | [Kent0625/bootstrap-coffee-farmers-income](https://github.com/Kent0625/bootstrap-coffee-farmers-income) |

---

## Project Overview

```{image} ../assets/projects/coffee-income-poster.png
:alt: From Farm to Cup bootstrap confidence interval project poster
:align: center
:width: 85%
```

### 1. Problem Statement
Agricultural income distributions in developing rural communities are frequently skewed, heavy-tailed, and subject to extreme climate and market volatility. Traditional parametric statistical methods (e.g., Student's t-interval) rely on normality assumptions that distort the true financial vulnerability of smallholder farmers. This study models farmer income uncertainty using empirical bootstrap methods to provide actionable, risk-aware policy insights for agricultural support programs.

### 2. Dataset & Sample Characteristics
- **Context:** Coffee growers across farming communities in Bukidnon, a premier coffee-producing province in the Philippines.
- **Sample:** 200 farmer financial and production records.
- **Key Variables:** Net annual harvest income, farm acreage, processing practices, and input expenditures.

### 3. Methodology
- **Resampling Strategy:** Generated 2,000 bootstrap replicates from the empirical distribution without making rigid parametric assumptions.
- **Interval Estimation:** Compared standard Normal-approximation intervals against Percentile intervals and Bias-Corrected and Accelerated (BCa) intervals to account for skewness and kurtosis.
- **Variance Analysis:** Analyzed how farm size and processing methods (wet vs. dry processing) impact the spread and lower-bound tail risk of farmer earnings.

### 4. Results & Policy Insights
- **Asymmetric Risk:** BCa intervals revealed that the true lower bound of net farmer earnings is significantly lower than suggested by classical parametric models.
- **Actionable Decision-Making:** Relying on simple mean earnings masks severe poverty risk during off-peak seasons; interval estimation provides government agencies and cooperatives with clearer thresholds for micro-subsidy allocation.

### 5. Tools & Technologies
- **Language & Libraries:** R, `boot`, `dplyr`, `ggplot2`, RMarkdown
- **Repository:** [Kent0625/bootstrap-coffee-farmers-income](https://github.com/Kent0625/bootstrap-coffee-farmers-income)
