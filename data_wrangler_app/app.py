import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from utils.session_manager import initialize_session, reset_session
from utils.loader import load_data
from utils.profiler import basic_profile
from utils.cleaning import handle_missing, handle_duplicates, convert_dtype
from utils.ai_recommender import generate_recommendations
from utils.auto_cleaner import auto_clean_dataset


# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI-Assisted Data Wrangler",
    layout="wide"
)

initialize_session()

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("📊 AI-Assisted Data Wrangler & Visualizer")

st.markdown(
"""
Clean, transform and visualize datasets interactively.
"""
)

st.divider()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Upload & Overview",
        "Cleaning Studio",
        "Visualization Builder",
        "AI Data Analyst",
        "Export & Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
"""
### Data Wrangling Tool

Clean • Transform • Visualize datasets

Built with:
- Python
- Pandas
- Streamlit
"""
)

st.sidebar.markdown("---")

# =================================================
# Upload & Overview
# =================================================
if page == "Upload & Overview":

    st.header("📂 Upload & Dataset Overview")

    if st.button("🔄 Reset Session"):
        reset_session()
        st.success("Session reset.")

    uploaded_file = st.file_uploader(
        "Upload dataset (CSV, Excel, JSON)",
        type=["csv", "xlsx", "xls", "json"]
    )

    if uploaded_file is not None and st.session_state["original_df"] is None:

        df = load_data(uploaded_file)

        if df is not None:

            st.session_state["original_df"] = df
            st.session_state["working_df"] = df.copy()

            st.success("Dataset uploaded successfully.")

    if st.session_state["working_df"] is not None:

        df = st.session_state["working_df"]

        profile = basic_profile(df)

        st.subheader("Dataset Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", profile["rows"])

        with col2:
            st.metric("Columns", profile["columns"])

        with col3:
            st.metric("Duplicates", profile["duplicates"])

        st.divider()

        st.subheader("Dataset Preview")

        st.dataframe(df.head())

        st.divider()

        st.subheader("Missing Values")

        st.dataframe(profile["missing"])

        st.divider()

        st.subheader("Column Data Types")

        st.dataframe(profile["dtypes"])

        st.divider()

        st.subheader("🤖 AI Cleaning Recommendations")

        recs = generate_recommendations(df)

        if len(recs) == 0:

            st.success("No major issues detected.")

        else:

            for r in recs:

                st.info(r)

# =================================================
# Cleaning Studio
# =================================================
elif page == "Cleaning Studio":

    st.header("🧹 Cleaning & Preparation Studio")

    if st.session_state["working_df"] is None:

        st.warning("Upload dataset first.")

    else:

        df = st.session_state["working_df"]

        st.subheader("🤖 AI Assistant")

        if st.button("✨ Auto Clean Dataset"):

            cleaned_df, log = auto_clean_dataset(df)

            st.session_state["working_df"] = cleaned_df

            for step in log:

                st.session_state["transformation_log"].append(
                    {"operation": step}
                )

            st.success("Dataset automatically cleaned!")

            for step in log:

                st.write("✔", step)

        st.divider()

        st.subheader("Missing Values")

        st.dataframe(df.isnull().sum())

        column = st.selectbox("Select column", df.columns)

        method = st.selectbox(
            "Method",
            [
                "Drop Rows",
                "Fill Constant",
                "Fill Mean",
                "Fill Median",
                "Fill Mode"
            ]
        )

        constant_value = None

        if method == "Fill Constant":

            constant_value = st.text_input("Enter constant value")

        if st.button("Apply Missing Value Handling"):

            updated_df, before_rows, after_rows = handle_missing(
                df,
                column,
                method,
                constant_value
            )

            st.session_state["working_df"] = updated_df

            st.success("Missing values handled.")

            st.write("Rows before:", before_rows)
            st.write("Rows after:", after_rows)

        st.divider()

        st.subheader("Duplicate Removal")

        subset = st.multiselect(
            "Columns for duplicate check",
            df.columns
        )

        keep_option = st.selectbox(
            "Keep option",
            ["first", "last"]
        )

        if st.button("Remove Duplicates"):

            updated_df, dup_df, before_rows, after_rows = handle_duplicates(
                df,
                subset if subset else None,
                keep_option
            )

            st.session_state["working_df"] = updated_df

            st.success("Duplicates removed.")

            st.write("Rows before:", before_rows)
            st.write("Rows after:", after_rows)

# =================================================
# Visualization Builder
# =================================================
elif page == "Visualization Builder":

    st.header("📈 Visualization Builder")

    if st.session_state["working_df"] is None:

        st.warning("Upload dataset first.")

    else:

        df = st.session_state["working_df"]

        chart_type = st.selectbox(
            "Chart type",
            [
                "Histogram",
                "Scatter Plot",
                "Bar Chart",
                "Correlation Heatmap"
            ]
        )

        if chart_type == "Histogram":

            col = st.selectbox(
                "Numeric column",
                df.select_dtypes(include="number").columns
            )

            fig = px.histogram(df, x=col)

            st.plotly_chart(fig)

        elif chart_type == "Scatter Plot":

            x = st.selectbox(
                "X column",
                df.select_dtypes(include="number").columns
            )

            y = st.selectbox(
                "Y column",
                df.select_dtypes(include="number").columns
            )

            fig = px.scatter(df, x=x, y=y)

            st.plotly_chart(fig)

        elif chart_type == "Bar Chart":

            cat = st.selectbox(
                "Category column",
                df.select_dtypes(
                    include=["object", "category"]
                ).columns
            )

            counts = df[cat].value_counts()

            fig = px.bar(
                x=counts.index,
                y=counts.values
            )

            st.plotly_chart(fig)

        elif chart_type == "Correlation Heatmap":

            num_df = df.select_dtypes(include="number")

            corr = num_df.corr()

            fig, ax = plt.subplots()

            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

            st.pyplot(fig)

# =================================================
# AI DATA ANALYST
# =================================================
elif page == "AI Data Analyst":

    st.header("🧠 AI Data Analyst")

    if st.session_state["working_df"] is None:

        st.warning("Upload a dataset first.")

    else:

        from utils.ai_chat import ask_ai_about_data

        df = st.session_state["working_df"]

        st.write("Ask questions about your dataset.")

        question = st.text_input(
            "Example: What factors affect the target variable?"
        )

        if st.button("Ask AI"):

            with st.spinner("Analyzing dataset..."):

                answer = ask_ai_about_data(df, question)

            st.success("AI Analysis")

            st.write(answer)

# =================================================
# Export
# =================================================
elif page == "Export & Report":

    st.header("📦 Export Cleaned Dataset")

    if st.session_state["working_df"] is None:

        st.warning("No dataset loaded.")

    else:

        df = st.session_state["working_df"]

        st.subheader("Transformation Log")

        for step in st.session_state["transformation_log"]:

            if isinstance(step, dict):

                st.write("✔", step["operation"])

            else:

                st.write("✔", step)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Cleaned Dataset",
            csv,
            "cleaned_dataset.csv",
            "text/csv"
        )

st.markdown("---")

st.markdown(
"""
AI-Assisted Data Wrangler & Visualizer  
Built for Data Wrangling & Visualization coursework
"""
)