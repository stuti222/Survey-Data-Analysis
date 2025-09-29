# survey_analysis.py
# -*- coding: utf-8 -*-

"""
Generalised Survey Data Analysis Script
=======================================

This script provides modular functions for:
- Inspecting metadata and nulls
- Checking unique values and duplicates
- Grouping and merging survey data
- Long-to-wide transformations
- Basic EDA and plotting
- Handling multi-select questions and age grouping
- Generating pseudo-code for DSL workflows

It is dataset-agnostic and works for any survey with:
- a raw data CSV (responses)
- a labels CSV (question metadata)

Author: OpenAI ChatGPT
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# Load CSV files
# ----------------------------
def load_data(raw_path: str, labels_path: str):
    raw_df = pd.read_csv(raw_path)
    labels_df = pd.read_csv(labels_path)
    return raw_df, labels_df

# ----------------------------
# Basic Inspection
# ----------------------------
def inspect_metadata(df, name="DataFrame"):
    print(f"\n{name}.shape: {df.shape}")
    print(df.info())
    print(df.columns.tolist())
    print(df.head())

def summarise_nulls(df, name="DataFrame"):
    print(f"\n=== Null Summary for {name} ===")
    print(df.isnull().sum().sort_values(ascending=False))
    print(df[df.isnull().any(axis=1)])

def check_uniques(df, columns):
    for col in columns:
        print(f"\nUnique values in {col}: {df[col].unique()}")

def check_duplicates(df, name="DataFrame"):
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows in {name}: {duplicates}")

# ----------------------------
# Grouping and Merging
# ----------------------------
def group_by_question_code(df, key='question_code'):
    return {code: group for code, group in df.groupby(key)}

def merge_labels(raw_df, labels_df):
    return raw_df.merge(labels_df, left_on='question_code', right_on='Question Code', how='left')

def compare_question_codes(raw_df, labels_df):
    raw_questions = set(raw_df['question_code'].unique())
    label_questions = set(labels_df['Question Code'].unique())
    print("\n=== Questions in raw not in labels ===", raw_questions - label_questions)
    print("=== Questions in labels not in raw ===", label_questions - raw_questions)

def summarise_answers(df):
    print("\n=== Unique answer codes per question ===")
    print(df.groupby('question_code')['answer_code'].nunique())

# ----------------------------
# Long-to-Wide Conversion
# ----------------------------
def long_to_wide(df, id_col='ID number', question_col='question_code', answer_col='answer_code', aggfunc='first'):
    if aggfunc == 'join_strings':
        def join_strings(x):
            return ','.join(str(v) for v in x.dropna().unique())
        aggfunc_to_use = join_strings
    else:
        aggfunc_to_use = aggfunc

    wide_df = df.pivot_table(
        index=id_col,
        columns=question_col,
        values=answer_col,
        aggfunc=aggfunc_to_use
    ).reset_index()

    if isinstance(wide_df.columns, pd.MultiIndex):
        wide_df.columns = [col if not isinstance(col, tuple) else col[-1] for col in wide_df.columns]

    return wide_df

# ----------------------------
# Plotting
# ----------------------------
def plot_answer_distribution(df, question_list):
    for q in question_list:
        subset = df[df['question_code'] == q]
        if not subset.empty:
            plt.figure()
            subset['answer_code'].value_counts(dropna=False).sort_index().plot(
                kind='bar', title=f'Answer Distribution for {q}', colour='skyblue'
            )
            plt.xlabel('Answer Code')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.show()

# ----------------------------
# Validation Functions
# ----------------------------
def validate_values(df, question_code, valid_values):
    answers = df[df['question_code'] == question_code]
    invalid = answers[~answers['answer_code'].isin(valid_values)]
    print(f"\n=== Invalid values for {question_code} ===")
    print(invalid)

def check_age_range(df, question_code, min_age=16, max_age=64):
    data = df[df['question_code'] == question_code].copy()
    data['answer_code'] = pd.to_numeric(data['answer_code'], errors='coerce')
    invalid = data[(data['answer_code'] < min_age) | (data['answer_code'] > max_age) | (data['answer_code'].isnull())]
    print(f"\n=== Invalid or Missing Ages in {question_code} ===")
    print(invalid)

def check_respondent_country(df, question_code, allowed_countries):
    respondents = df[df['question_code'] == question_code]['ID number'].unique()
    countries = df[df['question_code'] == 'Country'][['ID number', 'answer_code']]
    relevant = countries[countries['ID number'].isin(respondents)]
    invalid = relevant[~relevant['answer_code'].isin(allowed_countries)]
    print(f"\nRespondents answering {question_code} outside allowed countries:")
    print(invalid)
    if invalid.empty:
        print("All respondents are from allowed countries.")
    else:
        print(f"{len(invalid)} respondents are outside allowed countries.")

def cross_tab_summary(df):
    ct = df.groupby(['question_code', 'answer_code']).size().reset_index(name='count')
    print("\n=== Cross Tab Summary ===")
    print(ct)
    return ct

# ----------------------------
# Multi-select Handling
# ----------------------------
def generate_binary_columns(df, question_code, valid_range):
    q_df = df[df['question_code'] == question_code].copy()
    for val in valid_range:
        q_df[f'{question_code}_{val}'] = (q_df['answer_code'].astype(str) == str(val)).astype(int)
    q_df[f'{question_code}_Other'] = (q_df[[f'{question_code}_{v}' for v in valid_range]].sum(axis=1) == 0).astype(int)
    return q_df

def get_multiselect_respondents(df, base_col, valid_options):
    option_cols = [f"{base_col}_{i}" for i in valid_options]
    df[option_cols] = df[option_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    df[f'{base_col}_sum'] = df[option_cols].sum(axis=1)
    multi_df = df[df[f'{base_col}_sum'] > 1][['ID number'] + option_cols + [f'{base_col}_sum']].copy()
    return multi_df

# ----------------------------
# Age Grouping
# ----------------------------
def generate_age_group_dsl(origin, target, mapping):
    for group_id, age_range in mapping.items():
        min_age, max_age = age_range
        condition = f"({origin} >= {min_age}) & ({origin} <= {max_age})"
        print(f"Assign(condition='{condition}', target='{target}', value={group_id})")

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    raw_df, labels_df = load_data('raw_export.csv', 'labels.csv')

    inspect_metadata(raw_df, "raw_df")
    summarise_nulls(raw_df, "raw_df")
    check_duplicates(raw_df, "raw_df")
    check_uniques(raw_df, ['question_code', 'answer_code'])

    summarise_answers(raw_df)
    plot_answer_distribution(raw_df, ['q1', 'q2'])  # Example questions
    check_age_range(raw_df, 'q3', 16, 64)
    check_respondent_country(raw_df, 'q1', ['UK', 'USA', 'Greece'])

