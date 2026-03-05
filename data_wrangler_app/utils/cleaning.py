import pandas as pd


# ----------------------------
# Missing Value Handling
# ----------------------------
def handle_missing(df, column, method, value=None):

    before_rows = df.shape[0]

    if method == "Drop Rows":
        df = df.dropna(subset=[column])

    elif method == "Fill Constant":
        df[column] = df[column].fillna(value)

    elif method == "Fill Mean":
        df[column] = df[column].fillna(df[column].mean())

    elif method == "Fill Median":
        df[column] = df[column].fillna(df[column].median())

    elif method == "Fill Mode":
        df[column] = df[column].fillna(df[column].mode()[0])

    after_rows = df.shape[0]

    return df, before_rows, after_rows


# ----------------------------
# Duplicate Handling
# ----------------------------
def handle_duplicates(df, subset_columns=None, keep_option="first"):

    before_rows = df.shape[0]

    if subset_columns:
        duplicates_df = df[df.duplicated(subset=subset_columns, keep=False)]
        df = df.drop_duplicates(subset=subset_columns, keep=keep_option)
    else:
        duplicates_df = df[df.duplicated(keep=False)]
        df = df.drop_duplicates(keep=keep_option)

    after_rows = df.shape[0]

    return df, duplicates_df, before_rows, after_rows


# ----------------------------
# Data Type Conversion
# ----------------------------
def convert_dtype(df, column, target_type):

    try:

        if target_type == "numeric":
            df[column] = pd.to_numeric(df[column], errors="coerce")

        elif target_type == "string":
            df[column] = df[column].astype(str)

        elif target_type == "category":
            df[column] = df[column].astype("category")

        elif target_type == "datetime":
            df[column] = pd.to_datetime(df[column], errors="coerce")

        return df, True

    except Exception as e:
        return df, False