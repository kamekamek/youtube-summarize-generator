import streamlit as st
from main import TRANSLATIONS, get_text, initialize_session_state

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Settings | Summary Generator",
    page_icon="⚙️",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Load custom CSS
try:
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading CSS: {str(e)}")

st.title("⚙️ " + get_text('settings_title'))

# Development section
st.header(get_text('development_section'))
run_on_save = st.checkbox(
    get_text('run_on_save'),
    help=get_text('run_on_save_desc')
)

# Appearance section
st.header(get_text('appearance_section'))

# Wide mode setting
wide_mode = st.checkbox(
    get_text('wide_mode'),
    help=get_text('wide_mode_desc')
)

# Theme settings container
with st.container():
    st.subheader(get_text('theme_settings'))
    st.markdown(get_text('theme_colors_fonts'))
    
    # Theme selector
    theme = st.selectbox(
        "Theme",
        options=["Light", "Dark", "Custom"],
        index=0
    )

    # Language selector integrated in appearance section
    st.subheader(get_text('language_settings'))
    language_labels = {
        'ja': '日本語 (Japanese)',
        'en': 'English',
        'zh': '中文 (Chinese)'
    }

    selected_language = st.selectbox(
        label=get_text('language_settings'),
        options=['ja', 'en', 'zh'],
        index=['ja', 'en', 'zh'].index(st.session_state.language),
        format_func=lambda x: language_labels[x],
        key='language'
    )

    # Display current language
    st.info(f"{get_text('current_language')}: {language_labels[st.session_state.language]}")
