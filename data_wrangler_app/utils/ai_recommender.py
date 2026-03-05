import pandas as pd


def generate_recommendations(df):

    recommendations = []

    # -------------------------------------
    # Missing values
    # -------------------------------------
    missing = df.isnull().sum()

    for col in df.columns:

        if missing[col] > 0:

            if pd.api.types.is_numeric_dtype(df[col]):

                recommendations.append(
                    f"Fill missing values in '{col}' using Median"
                )

            else:

                recommendations.append(
                    f"Fill missing values in '{col}' using Mode"
                )

    # -------------------------------------
    # Object columns -> category
    # -------------------------------------
    for col in df.select_dtypes(include="object").columns:

        recommendations.append(
            f"Convert '{col}' to Category for better memory efficiency"
        )

    # -------------------------------------
    # Attendance improvement
    # -------------------------------------
    if "Attendance" in df.columns:

        if df["Attendance"].dtype == "float64":

            recommendations.append(
                "Convert 'Attendance' to Integer"
            )

    # -------------------------------------
    # Duplicate rows
    # -------------------------------------
    duplicates = df.duplicated().sum()

    if duplicates > 0:

        recommendations.append(
            f"Dataset contains {duplicates} duplicate rows. Consider removing them."
        )

    return recommendations