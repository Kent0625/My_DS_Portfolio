# The Life of a Bill

**Supervised Machine Learning Case Study: Predicting Philippine Senate Bill Status**

[![Live Model](https://img.shields.io/badge/Live_App-Hugging_Face_Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://kent0625-life-of-a-bill.hf.space)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)](https://github.com/Kent0625/ML_FINAL_PROJECT)
[![Model](https://img.shields.io/badge/Model-XGBoost-blue?style=flat-square)](https://xgboost.readthedocs.io/)

A supervised machine learning project that predicts Philippine Senate bill status from legislative records and explains which signals are most useful for understanding legislative movement.

---

## Key Metrics at a Glance

| Metric / Attribute | Value / Specification |
| :--- | :--- |
| **Dataset Size** | 7,352 Senate bill records (15th to 18th Congress) |
| **Selected Model** | XGBoost (Extreme Gradient Boosting) Classifier |
| **Holdout Macro F1** | 0.51 (multi-class imbalanced status prediction) |
| **Deployment** | Hugging Face Spaces (Interactive Gradio / Streamlit interface) |
| **Source Code** | [Kent0625/ML_FINAL_PROJECT](https://github.com/Kent0625/ML_FINAL_PROJECT) |

---

## Interactive Live Model

You can interact directly with the deployed model scenario evaluator below:

<iframe
    src="https://kent0625-life-of-a-bill.hf.space/?embed=true"
    frameborder="0"
    width="100%"
    height="600"
    style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"
></iframe>

*(If the Hugging Face Space is asleep, please allow a few moments for the container to wake up, or open it directly in [Hugging Face Spaces](https://kent0625-life-of-a-bill.hf.space).)*

---

## Project Overview

```{image} ../assets/projects/legislative-ml-pubmat.png
:alt: The Life of a Bill machine learning project poster
:align: center
:width: 85%
```

### 1. Problem Statement
Thousands of bills are introduced during each session of the Philippine Senate, yet only a tiny fraction progress through the committee level to Second Reading, Third Reading, and Republic Act enactment. Understanding which factors contribute to a bill's momentum is typically opaque. This project investigates whether structured bill metadata and textual attributes can reliably predict legislative progress and uncover systemic bottleneck patterns.

### 2. Dataset & Preprocessing
- **Source:** Official legislative archives spanning the 15th, 16th, 17th, and 18th Congresses of the Philippines.
- **Volume:** 7,352 structured bill records.
- **Features Engineered:**
  - Primary subject matter and policy classification
  - Authorship dynamics (principal sponsor, committee referrals)
  - Textual complexity and keyword length of long/short titles
  - Congressional session timing and filing chronology

### 3. Methodology & Modeling
- **Exploratory Data Analysis:** Highlighted severe class imbalance, with the vast majority of bills stalling at the Committee Stage.
- **Model Comparison:** Evaluated baseline Logistic Regression, Random Forests, LightGBM, and XGBoost.
- **Selected Architecture:** XGBoost Classifier optimized with stratified k-fold cross-validation.
- **Explainability:** Feature importance analysis via SHAP and gain metrics to determine which legislative features most strongly drive advancement.

### 4. Results & Key Findings
- **Macro F1:** 0.51 across holdout test sets, effectively distinguishing between early-stage and advanced bills despite heavy class imbalance.
- **Significance:** Sponsorship by key committee chairs and specific high-priority policy categorization (e.g., national budget, public health emergencies) showed the highest correlation with legislative advancement.

### 5. Tools & Technologies
- **Programming & Libraries:** Python, Pandas, NumPy, Scikit-Learn, XGBoost, Matplotlib, Seaborn
- **Deployment:** Hugging Face Spaces
- **Repository:** [Kent0625/ML_FINAL_PROJECT](https://github.com/Kent0625/ML_FINAL_PROJECT)
