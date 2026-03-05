import pandas as pd
import streamlit as st


@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        return None

    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)

    elif file_type == "json":
        df = pd.read_json(uploaded_file)

    else:
        raise ValueError("Unsupported file type")

    return df