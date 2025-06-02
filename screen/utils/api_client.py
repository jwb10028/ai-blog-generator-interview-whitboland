import requests
import json
from typing import Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def generate_blog(self, keyword: str) -> Dict[str, Any]:
        """Call the blog generation API endpoint"""
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "keyword": keyword
            }
            
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120  # 2 minute timeout for blog generation
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}: {response.text}"
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Could not connect to the API server. Make sure it's running on localhost:5000"
            }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Blog generation may take some time."
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }