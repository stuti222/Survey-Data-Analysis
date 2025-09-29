# Survey Data Analysis: Structured Approach

## Project Overview
This project demonstrates a structured approach to **survey data analysis**, transforming large, messy datasets into actionable insights. The goal is to clean, explore, validate, and visualise survey data efficiently while maintaining reproducibility and clarity.  

**Key Objective:** Implement an end-to-end exploratory data analysis (EDA) workflow to extract meaningful insights and ensure high data quality.

---

## Dataset
The dataset typically contains:

| Variable | Description |
|----------|-------------|
| `ID` | Unique respondent identifier |
| `question_code` | Code for each survey question |
| `answer_code` | Respondent’s answer |
| Other metadata | Country, demographic details, multi-select responses |

> Note: Datasets may include missing values, multi-select questions, or inconsistencies requiring validation.

---

## Methodology

### 1. Data Loading and Inspection
- Load datasets using `pandas.read_csv()`
- Inspect metadata: shape, columns, types
- Check for missing values and duplicates
- Explore unique values for key columns

### 2. Data Cleaning and Validation
- Handle missing values through imputation or removal
- Validate numeric ranges (e.g., age bounds)
- Correct inconsistent categorical responses (e.g., country codes)
- Flatten multi-select responses to wide format
- Use modular functions for repeated validation tasks

### 3. Exploratory Analysis
- **Categorical variables:** value counts, frequency distributions, cross-tabs
- **Numerical variables:** mean, median, variance, histograms
- **Relationships:** correlations, scatterplots, and heatmaps
- Identify patterns, outliers, and key drivers

### 4. Feature Engineering
- Encode categorical variables (one-hot or binary)
- Merge overlapping or related questions
- Derive new features for analysis
- Ensure features are interpretable and relevant

### 5. Visualisation
- Communicate insights effectively using:
  - Bar charts and histograms
  - Boxplots for outlier detection
  - Heatmaps for correlations
  - Cross-tab plots for multi-variable relationships

### 6. Modular Pipeline
- Organise EDA workflow into reusable modules:
  - `data_utils.py` – data loading and inspection
  - `transform_utils.py` – cleaning and reshaping
  - `analysis_utils.py` – summary statistics and cross-tabs
  - `eda_pipeline.py` – end-to-end execution
- Config-driven for flexibility with different datasets

---

## Tools and Libraries
- **Python:** primary language
- **Pandas:** data manipulation and cleaning
- **NumPy:** numerical operations
- **Matplotlib & Seaborn:** visualisation
- **Scipy / Statsmodels:** statistical testing

---

## Best Practices
- Maintain **modular, reusable code**
- Validate data at every stage
- Document assumptions and transformations
- Use visualisation to support conclusions
- Apply **statistical reasoning** logically

---

## Usage
1. Update `config.py` with dataset paths and relevant question codes.  
2. Run `python eda_pipeline.py` to perform a structured EDA.  
3. Explore individual modules for customisation or additional analyses.

---

## Outcome
Following this workflow allows you to:
- Quickly identify patterns, inconsistencies, and outliers
- Validate survey data rigorously
- Generate high-quality, reproducible insights
- Build a framework that can be adapted to future survey datasets
