# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    file = pd.read_csv(filepath)
    return file


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    if remove_duplicates == True:
        print("duplicate rows:")
        print(df.duplicated().sum())
        print(df.shape)
        clean_df = df.drop_duplicates()
        print("dropping the duplicates")
        print(clean_df.shape)
    else:
        print("keeping duplicates")
    
    if isinstance(sentinel_value, float) == True:
        clean_df.replace(sentinel_value,'NaN')
    print("data cleaned!")
    return clean_df 

    



def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    missing_val = df.isnull().sum()
    print(f"there are {missing_val} per a column ")
    return missing_val


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    df_fill = df.copy()
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if df[column].isnull().any():
        if strategy == 'mean':
            df_fill[column] = df[column].fillna(df[column].mean())
        elif strategy == 'median':
            df_fill[column] = df[column].fillna(df[column].median())
        elif strategy == 'ffill':
            df_fill[column] = df[column].ffill()
        else:
            raise ValueError("Strategy must be one of: 'mean', 'median', or 'ffill'.")
        print(f"changed missing values in {column} to {strategy} of column")
    else:
        print(f"No missing values found in '{column}'.")
    return df_fill



def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """
    fdf = df.copy()
    for filter in filters: 
        column_name = filter['column']
        value = filter['value']
        condition = filter['condition']
        if condition == 'equals':
            fdf = fdf[fdf[column_name] == value]
        elif condition == 'greater_than':
            fdf = fdf[fdf[column_name] > value]

        elif condition == 'less_than': 
            fdf = fdf[fdf[column_name] < value]
        
        elif condition == 'in_range': 
            val1 = value[0]
            val2 = value[1]
            fdf = fdf[(fdf[column_name] > val1) & (fdf[column_name] < val2)] 
        elif condition == 'in_list':
            fdf = fdf[fdf[column_name].isin(value)]

    return fdf
    


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    tdf = df.copy()
    for col, type, in type_map.items():
     if col in tdf.columns: #if the column in the type map is in the data frame
        print(f"{col} is present in the data frame")
        if type == 'datetime':
            tdf[col] = pd.to_datetime(tdf[col],errors='coerce')
            print(f"{col} was converted to datetime")
        elif type == 'numeric':
            tdf[col] = pd.to_numeric(tdf[col], errors = 'coerce')
            print(f"{col} was converted to numeric")
        elif type == 'category':
            tdf[col] = tdf[col].astype('category')
            print(f"{col} was converted to category")
        elif type == 'string':
            tdf[col] = tdf[col].astype('string')
            print(f"{col} was converted to string")
        else: 
            print("supported types are 'datetime', 'numeric', 'category', 'string'")
    
    return tdf



def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    bdf = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
    bdf[new_column]= (pd.cut(bdf[column],bins = bins,labels = labels, include_lowest = True))
    return bdf


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    pass




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
    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))