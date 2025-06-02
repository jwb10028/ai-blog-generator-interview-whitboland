import os
import json
import glob
from typing import List, Dict, Any

class FileUtils:
    def __init__(self, posts_directory: str = None):
        if posts_directory is None:
            # Default to the posts directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            self.posts_directory = os.path.join(project_root, "src", "posts")
        else:
            self.posts_directory = posts_directory
    
    def get_blog_posts(self) -> List[Dict[str, Any]]:
        blog_posts = []
        
        if not os.path.exists(self.posts_directory):
            return blog_posts
        
        # Find all JSON files in the posts directory
        json_files = glob.glob(os.path.join(self.posts_directory, "*.json"))
        
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                blog_posts.append({
                    "filename": os.path.basename(file_path),
                    "filepath": file_path,
                    "data": data
                })
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        return blog_posts
    
    def get_post_by_filename(self, filename: str) -> Dict[str, Any]:
        file_path = os.path.join(self.posts_directory, filename)
        
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}