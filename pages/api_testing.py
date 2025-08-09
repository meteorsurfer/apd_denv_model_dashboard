from utils.interface import clean_sb, nav_menu
from utils.markup import display_headline, display_footer
import streamlit as st 

st.set_page_config(page_title="APD | API Testing", page_icon="input/logo.svg", layout="wide", initial_sidebar_state="auto")
clean_sb()
nav_menu("/api_testing")

display_headline("Site Under Construction")  
st.info("Good things take time.")

display_footer()