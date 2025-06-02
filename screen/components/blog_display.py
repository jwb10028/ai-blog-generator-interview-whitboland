import streamlit as st
import json
from typing import List, Dict

class BlogDisplay:
    def __init__(self, file_utils):
        self.file_utils = file_utils
    
    def render(self):
        blog_posts = self.file_utils.get_blog_posts()
        
        if not blog_posts:
            st.info("No blog posts found. Generate your first blog post!")
            return
        
        # Sort by creation date (newest first)
        blog_posts.sort(key=lambda x: x['filename'], reverse=True)
        
        for post in blog_posts:
            self._render_blog_post(post)
    
    def _render_blog_post(self, post: Dict):
        with st.expander(f"{post['data']['keyword'].title()} - {post['filename']}", expanded=False):
            # SEO metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Search Volume", f"{post['data']['seo']['search_volume']:,}")
            
            with col2:
                st.metric("Keyword Difficulty", post['data']['seo']['keyword_difficulty'])
            
            with col3:
                st.metric("Avg CPC", f"${post['data']['seo']['avg_cpc']}")
            
            st.markdown("---")
            
            # Content preview
            content = post['data']['content']
            lines = content.split('\n')
            preview = '\n'.join(lines[:10])  # Show first 10 lines
            
            if len(lines) > 10:
                preview += "\n\n... (content truncated)"
            
            st.markdown(preview)
            
            # Action buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"View Full Content", key=f"view_{post['filename']}"):
                    st.session_state[f"show_full_{post['filename']}"] = True
            
            with col2:
                if st.button(f"Download JSON", key=f"download_{post['filename']}"):
                    st.download_button(
                        label="Download",
                        data=json.dumps(post['data'], indent=2),
                        file_name=post['filename'],
                        mime="application/json"
                    )
            
            # Show full content if requested
            if st.session_state.get(f"show_full_{post['filename']}", False):
                st.markdown("### Full Content:")
                st.markdown(post['data']['content'])
                if st.button(f"Hide Content", key=f"hide_{post['filename']}"):
                    st.session_state[f"show_full_{post['filename']}"] = False
                    st.rerun()