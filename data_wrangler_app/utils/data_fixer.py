import pandas as pd


def fix_dataset(df):

    df = df.copy()

    # ---------------------------------------
    # Fix Attendance column (lowercase now)
    # ---------------------------------------
    if "attendance" in df.columns:

        # Fill missing values first
        if df["attendance"].isnull().sum() > 0:

            df["attendance"] = df["attendance"].fillna(
                df["attendance"].median()
            )

        # Convert to integer
        df["attendance"] = df["attendance"].astype(int)

    # ---------------------------------------
    # Standardize text formatting
    # ---------------------------------------
    text_columns = ["gender", "background", "major", "target"]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )

    # ---------------------------------------
    # Convert to categorical type
    # ---------------------------------------
    categorical_columns = ["gender", "background", "major", "target"]

    for col in categorical_columns:

        if col in df.columns:

            df[col] = df[col].astype("category")

    return df
