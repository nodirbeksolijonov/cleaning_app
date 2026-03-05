import pandas as pd
import numpy as np
from utils.data_fixer import fix_dataset


def auto_clean_dataset(df):

    cleaned_df = df.copy()
    log = []

    # ------------------------------------------------
    # Normalize column names
    # ------------------------------------------------
    cleaned_df.columns = (
        cleaned_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    log.append("Normalized column names")

    # ------------------------------------------------
    # Fix dataset structure (from data_fixer)
    # ------------------------------------------------
    cleaned_df = fix_dataset(cleaned_df)

    log.append("Standardized text formatting")
    log.append("Converted categorical columns")

    # ------------------------------------------------
    # Convert numeric strings to numbers
    # ------------------------------------------------
    for col in cleaned_df.columns:

        if cleaned_df[col].dtype == "object":

            try:

                cleaned_df[col] = pd.to_numeric(cleaned_df[col])

                log.append(f"Converted '{col}' to numeric")

            except:
                pass

    # ------------------------------------------------
    # Fill missing values
    # ------------------------------------------------
    for col in cleaned_df.columns:

        if cleaned_df[col].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(cleaned_df[col]):

                cleaned_df[col].fillna(
                    cleaned_df[col].median(),
                    inplace=True
                )

                log.append(
                    f"Filled missing values in '{col}' using Median"
                )

            else:

                cleaned_df[col].fillna(
                    cleaned_df[col].mode()[0],
                    inplace=True
                )

                log.append(
                    f"Filled missing values in '{col}' using Mode"
                )

    # ------------------------------------------------
    # Remove duplicate rows
    # ------------------------------------------------
    duplicates = cleaned_df.duplicated().sum()

    if duplicates > 0:

        cleaned_df = cleaned_df.drop_duplicates()

        log.append(f"Removed {duplicates} duplicate rows")

    # ------------------------------------------------
    # Remove constant columns
    # ------------------------------------------------
    for col in cleaned_df.columns:

        if cleaned_df[col].nunique() <= 1:

            cleaned_df.drop(columns=[col], inplace=True)

            log.append(f"Removed constant column '{col}'")

    # ------------------------------------------------
    # Outlier detection (IQR method)
    # ------------------------------------------------
    numeric_cols = cleaned_df.select_dtypes(include=np.number).columns

    for col in numeric_cols:

        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        before = cleaned_df[col].copy()

        cleaned_df[col] = cleaned_df[col].clip(lower, upper)

        if not before.equals(cleaned_df[col]):

            log.append(f"Capped outliers in '{col}'")

    return cleaned_df, log