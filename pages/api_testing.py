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
        <div style="font-family: 'Segoe UI', sans-serif; line-height: 1.6; font-size: 15px;">
        <h3>🧠 Modeling Framework</h3>
        <p><strong>Microsoft LightGBM</strong> (optimized for imbalanced WHO-backed outbreak thresholding)</p>

        <h3>📦 Language & IDEs</h3>
        <ul>
            <li><code>Python</code></li>
            <li><code>Jupyter Notebook</code></li>
            <li><code>VS Code</code></li>
        </ul>

        <h3>🌐 Data Gathering & Preparation</h3>
        <ul>
            <li><code>pandas</code>, <code>GeoPandas</code>, <code>requests</code>, <code>concurrent.futures</code></li>
            <li><code>QGIS</code></li>
        </ul>

        <h3>📊 Exploratory Data Analysis</h3>
        <ul>
            <li><code>matplotlib</code>, <code>seaborn</code>, <code>pandas</code>, <code>Streamlit</code></li>
        </ul>

        <h3>🔍 Modeling & Optimization</h3>
        <ul>
            <li><code>scikit-learn</code>, <code>NumPy</code>, <code>LightGBM</code>, <code>XGBoost</code>, <code>CatBoost</code>, <code>Optuna</code></li>
        </ul>

        <h3>🚀 Deployment & Version Control</h3>
        <ul>
            <li><code>Flask</code>, <code>Streamlit</code>, <code>Git</code>, <code>GitHub</code></li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

display_footer()