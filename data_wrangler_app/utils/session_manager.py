import streamlit as st


def initialize_session():
    if "original_df" not in st.session_state:
        st.session_state["original_df"] = None

    if "working_df" not in st.session_state:
        st.session_state["working_df"] = None

    if "transformation_log" not in st.session_state:
        st.session_state["transformation_log"] = []

    if "undo_stack" not in st.session_state:
        st.session_state["undo_stack"] = []


def reset_session():
    st.session_state["working_df"] = st.session_state["original_df"]
    st.session_state["transformation_log"] = []
    st.session_state["undo_stack"] = []