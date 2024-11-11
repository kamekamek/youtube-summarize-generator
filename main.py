import streamlit as st
import os
from utils import YouTubeHandler, GeminiProcessor

# Page configuration
st.set_page_config(
    page_title="YouTube Video Article Generator",
    page_icon="📝",
    layout="wide"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'generated_article' not in st.session_state:
        st.session_state.generated_article = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def validate_urls(urls: list) -> list:
    """Validate YouTube URLs."""
    valid_urls = []
    for url in urls:
        if url.strip() and ('youtube.com' in url or 'youtu.be' in url):
            valid_urls.append(url.strip())
    return valid_urls

def main():
    initialize_session_state()
    
    st.title("📝 YouTube Video Article Generator")
    st.markdown("""
    Transform multiple YouTube videos into a comprehensive article using AI.
    Enter YouTube video URLs (one per line) below.
    """)

    # Input area for YouTube URLs
    urls_input = st.text_area(
        "Enter YouTube URLs (one per line)",
        height=150,
        help="Paste YouTube URLs, one per line"
    )

    # Process button
    if st.button("Generate Article", disabled=st.session_state.processing):
        urls = urls_input.split('\n')
        valid_urls = validate_urls(urls)

        if not valid_urls:
            st.error("Please enter valid YouTube URLs")
            return

        try:
            st.session_state.processing = True

            # Initialize handlers with environment variables
            youtube_handler = YouTubeHandler(api_key=os.environ['YOUTUBE_API_KEY'])
            gemini_processor = GeminiProcessor(api_key=os.environ['GEMINI_API_KEY'])

            # Process videos
            with st.spinner("Processing videos..."):
                video_data = youtube_handler.process_videos(valid_urls)

            # Check for errors
            errors = [data for data in video_data if 'error' in data]
            if errors:
                for error in errors:
                    st.error(f"Error processing {error['url']}: {error['error']}")
                if len(errors) == len(video_data):
                    return

            # Generate article
            with st.spinner("Generating article..."):
                article = gemini_processor.generate_article(video_data)
                st.session_state.generated_article = article

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            st.session_state.processing = False

    # Display generated article
    if st.session_state.generated_article:
        st.markdown("### Generated Article")
        st.markdown('<div class="article-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_article)
        st.markdown('</div>', unsafe_allow_html=True)

        # Source attribution
        st.markdown("### Sources")
        for url in validate_urls(urls_input.split('\n')):
            st.markdown(f'<a href="{url}" class="source-link" target="_blank">{url}</a>', 
                       unsafe_allow_html=True)

if __name__ == "__main__":
    main()
