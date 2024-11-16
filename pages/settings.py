import streamlit as st
from main import TRANSLATIONS, get_text, initialize_session_state

# Initialize session state
initialize_session_state()

# Page config
st.set_page_config(
    page_title="Settings | Summary Generator",
    page_icon="⚙️",
    layout="wide"
)

# Load custom CSS
try:
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading CSS: {str(e)}")

st.title("⚙️ " + get_text('settings_section'))

# Language settings section
st.header(get_text('language_selector'))

# Language selector with more detailed labels
language_labels = {
    'ja': '日本語 (Japanese)',
    'en': 'English',
    'zh': '中文 (Chinese)'
}

selected_language = st.selectbox(
    "Application Language / 言語設定 / 语言设置",
    options=['ja', 'en', 'zh'],
    index=['ja', 'en', 'zh'].index(st.session_state.language),
    format_func=lambda x: language_labels[x],
    key='language'
)

# Display current language settings
st.info(f"Current language / 現在の言語 / 当前语言: {language_labels[st.session_state.language]}")
