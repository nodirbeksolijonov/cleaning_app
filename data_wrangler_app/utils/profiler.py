import pandas as pd


def basic_profile(df):

    profile = {}

    # Shape
    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]

    # Column names
    profile["column_names"] = df.columns.tolist()

    # Data types
    profile["dtypes"] = df.dtypes.astype(str)

    # Missing values
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percent.round(2)
    })

    profile["missing"] = missing_df

    # Duplicate count
    profile["duplicates"] = df.duplicated().sum()

    return profile