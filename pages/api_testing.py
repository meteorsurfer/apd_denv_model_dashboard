from utils.interface import clean_sb, nav_menu
from utils.markup import display_headline, display_footer, display_sample_outbreak_news,predict_dengue_risk_3_months
import streamlit as st 

st.set_page_config(page_title="APD | API Testing", page_icon="input/logo.svg", layout="wide", initial_sidebar_state="collapsed")
clean_sb()
nav_menu("/api_testing")

display_headline("Predicting 3-Month Dengue Outbreak Risk from Current Weather Patterns")  

col1, col2 = st.columns([1, 1])

with col2:
    predict_dengue_risk_3_months()

with col1: 
    display_sample_outbreak_news("input/")

with st.expander("End-to-End ML Lifecycle Tech Stack"):
    st.markdown("""
    **🧠 Modeling Framework:** Microsoft LightGBM (optimized for imbalanced WHO-backed outbreak levels)  
    **📦 Language & IDEs:** `Python`, `Jupyter Notebook`, VS Code  
    **🌐 Data Gathering & Preparation:** `pandas`, `GeoPandas`, `requests`, `concurrent.futures`  
    **📈 Exploratory Data Analysis:** `matplotlib`, `seaborn`, `pandas`, `Streamlit`  
    **🔍 Modeling & Optimization:** `scikit-learn`, `NumPy`, `LightGBM`, `XGBoost`, `CatBoost`, `Optuna`  
    **🚀 Deployment & Version Control:** `Flask`, `Streamlit`, `Git`, `GitHub`  
    """, unsafe_allow_html=True)

display_footer()