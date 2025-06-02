import streamlit as st
import os
import sys

# Add the parent directory to the path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.blog_display import BlogDisplay
from components.keyword_form import KeywordForm
from utils.api_client import APIClient
from utils.file_utils import FileUtils

def main():
    st.set_page_config(
        page_title="AI Blog Generator",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("🤖 AI Blog Generator")
    st.markdown("---")
    
    # Initialize components
    api_client = APIClient()
    file_utils = FileUtils()
    blog_display = BlogDisplay(file_utils)
    keyword_form = KeywordForm(api_client)
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Generate New Blog")
        keyword_form.render()
    
    with col2:
        st.header("Existing Blog Posts")
        blog_display.render()

if __name__ == "__main__":
    main()