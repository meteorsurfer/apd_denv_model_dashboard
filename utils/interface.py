import streamlit as st

UI_CLEAN = st.secrets["UI_CLEAN"]

def clean_sb():
    st.markdown(UI_CLEAN, unsafe_allow_html=True)
    return

def nav_menu(current_page):
    pages = {
        "Exploratory Data Analysis": "/",
        "Machine Learning Model Testing": "/api_testing",
    }
    if current_page and current_page in pages.values():
        current_page_pair = next((k, v) for k, v in pages.items() if v == current_page)
        remaining_pages = {k: v for k, v in pages.items() if v != current_page}
        sorted_pages = dict(sorted(remaining_pages.items()))
        pages = {current_page_pair[0]: current_page_pair[1], **sorted_pages}
    selected_page = st.sidebar.selectbox(
        "Navigate to:", 
        list(pages.keys()),
        index=0
    )
    if st.session_state.get('last_page') != selected_page:
        if 'last_page' in st.session_state:
            st.query_params["page"] = selected_page
            st.markdown(
                f'<meta http-equiv="refresh" content="0; url={pages[selected_page]}">', 
                unsafe_allow_html=True
            )
            st.stop()
        st.session_state['last_page'] = selected_page
    return
