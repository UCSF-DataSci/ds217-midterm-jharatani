# TODO: Add shebang line: 
#!/usr/bin/env python3

# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


filepath = 'data/clinical_trial_raw.csv'

def load_data(filepath: str) -> pd.DataFrame:

    df = pd.read_csv(filepath)

    return df


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    df_clean = df.copy()
     
    if remove_duplicates:
        df_clean = df.drop_duplicates()

    if sentinel_value is not None:
        df_clean = df_clean.replace(sentinel_value, np.nan)

    if "bmi" in df_clean.columns:
        df_clean.loc[df_clean["bmi"] <= 0, "bmi"] = np.nan #Found -1 BMI value later in analysis and came back to account for this in cleaning

   
    return df_clean


    


def detect_missing(df: pd.DataFrame) -> pd.Series:


    return df.isnull().sum()




def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:

    df_filled = df.copy()

    if strategy == 'mean':
        fill_value = df[column].mean()
    elif strategy == 'median':
        fill_value = df[column].median()
    elif strategy == 'ffill':
        df[column] = df[column].fillna(method='ffill')
        return df
    else:
        raise ValueError("Unsupported strategy. Use 'mean', 'median', or 'ffill'.")

    df_filled[column] = df[column].fillna(fill_value)
    return df_filled


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    df_filtered = df.copy()    

    for f in filters:
        col = f['column']
        cond = f['condition']
        val = f['value']

        if cond == 'equals':
            df_filtered = df_filtered[df_filtered[col] == val]
        elif cond == 'greater_than':
            df_filtered = df_filtered[df_filtered[col] > val]
        elif cond == 'less':
            df_filtered = df_filtered[df_filtered[col] < val]
        elif cond == 'in_range':
            df_filtered = df_filtered[(df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])]
        elif cond == 'in_list':
            df_filtered = df_filtered[df_filtered[col].isin(val)]
        else:
            raise ValueError(f"Unsupported condition: {cond}")  
        
    return df_filtered
    


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:

    df_typed = df.copy()

    for col, target_type in type_map.items():
        if target_type == 'datetime':
            df_typed[col] = pd.to_datetime(df_typed[col], errors='coerce')
        elif target_type == 'numeric':
            df_typed[col] = pd.to_numeric(df_typed[col], errors='coerce')
        elif target_type == 'category':
            df_typed[col] = df_typed[col].astype('category')
        elif target_type == 'string':
            df_typed[col] = df_typed[col].astype('string')
        else:
            raise ValueError(f"Unsupported target type: {target_type}")
        
        return df_typed



def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    
    df_binned = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
    df_binned[new_column] = pd.cut(df_binned[column], bins=bins, labels=labels, include_lowest=True)
    return df_binned




def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    
    if agg_dict is None:
        summary = df.groupby(group_col).describe()
    else:
        summary = df.groupby(group_col).agg(agg_dict)
    return summary




if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")

    df = load_data('data/clinical_trial_raw.csv')
    # ✅ check that DataFrame loaded correctly
    print("Shape:", df.shape)
    print("Columns:", df.columns)
    print(df.head())      # shows first 5 rows
    print(df.info())
    print(type(df))

    df_clean = clean_data(df, remove_duplicates = True, sentinel_value=-999)
    # ✅ check that cleaning works
    print("After cleaning, missing values per column:")
    print(detect_missing(df_clean))

   
    df_filled = df_clean.copy()
    for col in df_filled.select_dtypes(include=['number']).columns:
        df_filled = fill_missing(df_filled, col, strategy='mean')

        df_filled = df_filled.round(0)
    # ✅ check that filling works
    print("After filling missing column values:")
    print(detect_missing(df_filled))

    df_filtered = filter_data(
        df_filled,
        filters=[
            {'column': 'age', 'condition': 'greater_than', 'value': 18},
            {'column': 'age', 'condition': 'less', 'value': 65},
            {'column': 'site', 'condition': 'in_list', 'value': ['Site A','Site C', 'Site E']},
        ]
    )
    # ✅ check that filtering works
    print("After filtering, shape:", df_filtered.shape)

    df_typed = transform_types(df_filtered, type_map={
        'enrollment_date': 'datetime',
        'age': 'numeric',
        'site': 'category'
    })
    # ✅ check that type transformation works
    print("After type transformation, dtypes:")
    print(df_typed.dtypes)
    # columns that should be categorical
    cat_cols = ["site", "sex", "intervention_group", "outcome_cvd", "dropout"]

    df_typed2 = df_typed.copy()
    for c in cat_cols:
        if c in df_typed2.columns:
            df_typed2[c] = df_typed2[c].astype("category")


    nullable_int_cols = ["follow_up_months", "adverse_events"]
    for c in nullable_int_cols:
        if c in df_typed2.columns:
            df_typed2[c] = pd.to_numeric(df_typed2[c], errors="coerce").astype("Int64")

    print(df_typed2.dtypes)


    df_binned = create_bins(
        df_typed2,
        column='age',
        bins=[0, 18, 35, 50, 65, 100],
        labels=['<18', '18-34', '35-49', '50-64', '65+']
    )
    # ✅ check that binning works
    print("After binning, unique age bins:")
    print(df_binned['age_binned'].unique())

# Clean and standardize site names and intervention groups
    for col in ["site", "intervention_group"]:
        df_filled[col] = (
         df_filled[col]
            .str.strip()
            .str.replace("_", " ")
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
    )

# Apply custom fixes for intervention_group
    df_filled["intervention_group"] = (
        df_filled["intervention_group"]
        .str.replace("Treatmenta", "Treatment A")
        .str.replace("Treatmen A", "Treatment A")
        .str.replace("Contrl", "Control")
    )


    summary = summarize_by_group(
        df_filled, 'site',
        {'age': ['mean','std'], 'bmi': 'mean'}
    )
    # ✅ check that grouping and aggregation works
    print("Summary statistics by site:")
    print(summary)

    df_final = df_filled.copy()
    df_final.to_csv('output/clinical_trial_cleaned.csv', index=False)
    print("Cleaned data saved to 'output/clinical_trial_cleaned.csv'")