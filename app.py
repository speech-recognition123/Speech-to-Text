from applications import visualizations, viz_model
from multiapp import MultiApp
import os
import sys
import streamlit as st

sys.path.insert(0, './scripts')


st.set_page_config(page_title="Speech to Text", layout="wide")


app = MultiApp()

st.sidebar.markdown("""
# Speech to Text
""")
