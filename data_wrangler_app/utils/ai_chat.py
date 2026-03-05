from dotenv import load_dotenv
import os
import pandas as pd
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def dataframe_summary(df):

    summary = {
        "columns": list(df.columns),
        "rows": len(df),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }

    # Add numeric statistics if available
    try:
        summary["statistics"] = df.describe().to_dict()
    except:
        summary["statistics"] = {}

    return summary


def ask_ai_about_data(df, question):

    summary = dataframe_summary(df)

    prompt = f"""
You are a professional data analyst.

A user uploaded a dataset. Here is the dataset summary.

Number of rows: {summary['rows']}

Columns:
{summary['columns']}

Column Data Types:
{summary['dtypes']}

Missing Values:
{summary['missing_values']}

Basic Statistics:
{summary['statistics']}

User Question:
{question}

Please analyze the dataset information and answer the user's question clearly.
If possible, give insights or recommendations.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional data scientist helping analyze datasets."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content