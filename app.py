from utils.interface import clean_sb, nav_menu
from utils.wrangling import load_eda_data, dataset_info
from utils.markup import display_headline, display_metadata, visualize_denv_per_categories, visualize_geographic_cases,visualize_trend, region_month_cases_density, display_footer
import streamlit as st 


st.set_page_config(page_title="APD | Exploratory Data Analysis", page_icon="input/logo.svg", layout="wide", initial_sidebar_state="auto")
clean_sb()
nav_menu("/app")

display_headline("Exploratory Analysis of Dengue Cases Across Philippine Regions (2016–2023)")  

df = load_eda_data()
display_metadata(dataset_info(df))

col1, col2 = st.columns([1,1])

with col1:

    st.markdown(
        """
        <div style='text-align: center; color: white;'>
           Median Dengue Cases Per Location (2016-2023)
        </div>
        """,
        unsafe_allow_html=True
    )

    visualize_geographic_cases(df)

    st.write("")
    st.write("")
    st.write("")

    st.markdown(
        """
        <div style='text-align: center; color: white;'>
           Density Map for Dengue Cases Per Region and Month (2016-2023)
        </div>
        """,
        unsafe_allow_html=True
    )

    region_month_cases_density(df)


with col2:

    st.markdown(
        """
        <div style='text-align: center; color: white;'>
           Median Dengue Cases Per Category (2016-2023)
        </div>
        """,
        unsafe_allow_html=True
    )

    visualize_denv_per_categories(df)

    st.markdown(
        """
        <div style='text-align: center; color: white;'>
            Median Dengue Cases Per Region Trend (2016-2023)
        </div>
        """,
        unsafe_allow_html=True
    )

    visualize_trend(df)


display_footer()