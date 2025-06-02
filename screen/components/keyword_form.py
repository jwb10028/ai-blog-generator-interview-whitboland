import streamlit as st
from typing import Optional

class KeywordForm:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def render(self):
        with st.form("keyword_form"):
            st.markdown("### Enter a keyword to generate a blog post")
            
            keyword = st.text_input(
                "Keyword",
                placeholder="e.g., wireless earbuds, smart watches, etc.",
                help="Enter a keyword or phrase for blog generation"
            )
            
            submitted = st.form_submit_button("Generate Blog Post")
            
            if submitted:
                if keyword.strip():
                    self._handle_submission(keyword.strip())
                else:
                    st.error("Please enter a keyword")
    
    def _handle_submission(self, keyword: str):
        """Handle form submission"""
        with st.spinner(f"Generating blog post for '{keyword}'..."):
            try:
                result = self.api_client.generate_blog(keyword)
                
                if result['success']:
                    st.success(f"Blog post generated successfully!")
                    st.info(f"Saved as: {result['filename']}")
                    
                    # Show a preview of the generated content
                    if 'data' in result:
                        with st.expander("Preview Generated Content", expanded=True):
                            data = result['data']
                            
                            # Show SEO metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Search Volume", f"{data['seo']['search_volume']:,}")
                            with col2:
                                st.metric("Keyword Difficulty", data['seo']['keyword_difficulty'])
                            with col3:
                                st.metric("Avg CPC", f"${data['seo']['avg_cpc']}")
                            
                            # Show content preview
                            content_lines = data['content'].split('\n')
                            preview = '\n'.join(content_lines[:8])
                            st.markdown(preview + "\n\n... (preview truncated)")
                    
                    # Auto-refresh to show new post in the list
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error occurred')}")
            
            except Exception as e:
                st.error(f"Error generating blog post: {str(e)}")