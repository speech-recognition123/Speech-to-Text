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

with open('./scripts/web-css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add all your application here
app.add_app("visualizations", visualizations.app)
app.add_app("model-prediction", viz_model.app)

# The main app
app.run()
