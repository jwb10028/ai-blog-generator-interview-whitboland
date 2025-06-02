from flask import Flask, request, jsonify
from dotenv import load_dotenv
from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
from datetime import datetime
import re

# Environment vars
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Scheduler configuration (interval in days)
SCHEDULER_GENERATION_INTERVAL = 1
SCHEDULER_GENERATION_KEYWORD = "wireless earbuds"

# Init Flask app
app = Flask(__name__)

# Define the endpoints
@app.route('/generate', methods=['GET'])
def generate():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Missing required parameter: keyword"}), 400

    # Get SEO data
    seo_data = fetch_seo_data(keyword)

    # Generate blog post
    blog_post = generate_blog_post(keyword, seo_data)

    # Save JSON output to disk for UI
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"posts/{keyword.replace(' ', '_')}_{timestamp}.json"
    os.makedirs("posts", exist_ok=True)
    with open(filename, "w") as f:
        json.dump({"keyword": keyword, "seo": seo_data, "content": blog_post}, f, indent=2)

    def linkify(text):
        return re.sub(
            r'(https?://[^\s]+)',
            r'<a href="\1" target="_blank">\1</a>',
            text
        )
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Blog Post: {keyword}</title>
        </head>
        <body>
            <h1>{keyword}</h1>
            <p><strong>Search Volume:</strong> {seo_data['search_volume']}</p>
            <p><strong>Keyword Difficulty:</strong> {seo_data['keyword_difficulty']}</p>
            <p><strong>Avg CPC:</strong> ${seo_data['avg_cpc']}</p>
            <hr>
            <div>{linkify(blog_post).replace('\n', '<br>')}</div>
        </body>
        </html>
        """

    # Save HTML to disk
    os.makedirs("html", exist_ok=True)
    html_filename = f"html/{keyword.replace(' ', '_')}_{timestamp}.html"
    with open(html_filename, "w") as f:
        f.write(html_content)

    return jsonify({
        "keyword": keyword,
        "seo_data": seo_data,
        "blog_post": blog_post
    })


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify({
            "success": False,
            "error": "Missing required parameter: keyword"
        }), 400
    
    keyword = data['keyword']
    
    try:
        # Call the GET endpoint internally
        with app.test_client() as client:
            response = client.get(f'/generate?keyword={keyword}')
            
        if response.status_code == 200:
            result_data = response.get_json()
            
            # Calculate filename for response
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"{keyword.replace(' ', '_')}_{timestamp}.json"
            
            return jsonify({
                "success": True,
                "keyword": keyword,
                "filename": filename,
                "data": {
                    "keyword": keyword,
                    "seo": result_data["seo_data"],
                    "content": result_data["blog_post"]
                },
                "message": f"Blog post generated successfully for '{keyword}'"
            })
        else:
            error_data = response.get_json()
            return jsonify({
                "success": False,
                "error": error_data.get("error", "Unknown error occurred")
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error generating blog post: {str(e)}"
        }), 500


# Schedule a daily generation job
def scheduled_job():
    keyword = SCHEDULER_GENERATION_KEYWORD
    seo_data = fetch_seo_data(keyword)
    blog_post = generate_blog_post(keyword, seo_data)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"posts/daily_report_{SCHEDULER_GENERATION_KEYWORD}_{timestamp}.json"
    os.makedirs("posts", exist_ok=True)
    with open(filename, "w") as f:
        json.dump({"keyword": keyword, "seo": seo_data, "content": blog_post}, f, indent=2)

    print(f"[{timestamp}] Blog post generated for keyword: {keyword}")


# Register APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', days=SCHEDULER_GENERATION_INTERVAL)
scheduler.start()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
