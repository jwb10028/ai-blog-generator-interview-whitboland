# AI Blog Generator - Flask Application

An automated SEO-focused blog post generator that leverages OpenAI's GPT models to create structured content with affiliate links. This Flask-based application performs "SEO research" through mock data and generates daily blog posts automatically.

## Project Overview

This application demonstrates a complete AI-powered content generation pipeline, featuring:

- **SEO Research Simulation**: Mock SEO data with search volume, keyword difficulty, and cost-per-click metrics
- **AI Content Generation**: OpenAI integration for creating structured blog posts with affiliate link placeholders
- **Automated Scheduling**: Daily cron job functionality for consistent content creation
- **RESTful API**: Clean Flask endpoints for both interactive and programmatic access
- **File-based Storage**: JSON output with timestamped files for easy tracking

## How All Deliverables Were Covered

### ✅ **Core Flask Application (app.py)**

**Deliverable**: A Flask app exposing at least one endpoint

**Implementation**: 
- **Primary Endpoint**: `GET /generate?keyword=<your_keyword>` - Main content generation endpoint
- **UI Post Endpoint**: `POST /api/generate` - JSON-based API for programmatic access

```python
@app.route('/generate', methods=['GET'])
def generate():
    keyword = request.args.get('keyword')
    # ... SEO data fetching and blog generation logic
    
@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json()
    # ... JSON-based request handling
```

### ✅ **SEO Research Module (seo_fetcher.py)**

**Deliverable**: A module that returns `search_volume`, `keyword_difficulty`, and `avg_cpc`

**Implementation**: Mock SEO database with realistic metrics for popular keywords

```python
def fetch_seo_data(keyword):
    mock_database = {
        "wireless earbuds": {
            "search_volume": 120000,
            "keyword_difficulty": 37,
            "avg_cpc": 1.25
        },
        # ... more keywords with real-world data patterns
    }
```

**Features**:
- Pre-configured data for common keywords (wireless earbuds, standing desk, etc.)
- Fallback default metrics for unknown keywords
- Realistic SEO metrics based on industry standards

### ✅ **AI Content Generation (ai_generator.py)**

**Deliverable**: A module that calls OpenAI with structured prompts and replaces `{{AFF_LINK_n}}` placeholders

**Implementation**: GPT-powered blog post generation with SEO-optimized prompts

```python
def generate_blog_post(keyword, seo_data):
    prompt = f"""
    You are an SEO copywriter. Write a well-structured blog post about "{keyword}".
    
    Include:
    - An engaging introduction
    - A subheading on why {keyword} is trending (mention search volume: {search_volume})
    - A subheading on challenges/competition (mention keyword difficulty: {difficulty})
    - 2–3 product recommendations with affiliate link placeholders
    - A conclusion with call to action
    """
```

**Features**:
- Structured prompts incorporating SEO data
- Automatic replacement of `{{AFF_LINK_1}}`, `{{AFF_LINK_2}}`, etc. with dummy URLs
- Configurable model selection (gpt-3.5-turbo by default)
- Temperature control for content variability

### ✅ **Automated Scheduling System**

**Deliverable**: Either APScheduler job OR shell script + crontab setup

**Implementation**: APScheduler with daily background job execution

```python
def scheduled_job():
    keyword = SCHEDULER_GENERATION_KEYWORD  # "wireless earbuds"
    seo_data = fetch_seo_data(keyword)
    blog_post = generate_blog_post(keyword, seo_data)
    # ... save to timestamped file

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', days=SCHEDULER_GENERATION_INTERVAL)
scheduler.start()
```

**Configuration**:
- `SCHEDULER_GENERATION_INTERVAL = 1` (daily execution)
- `SCHEDULER_GENERATION_KEYWORD = "wireless earbuds"` (default keyword)
- Background execution doesn't block the Flask application
- Automatic file saving with timestamps

### ✅ **File Management & Output Structure**

**Deliverable**: HTML output stored locally with proper organization

**Implementation**: Organized file structure with timestamps and keyword-based naming

```
src/html/
├── wireless_earbuds_20250602-100430.html
├── smart_watches_20250602-103143.html
├── 3D_Printers_20250602-103306.html
└── daily_report_wireless_earbuds_YYYYMMDD-HHMMSS.html
```



## Technical Architecture

### Flask Application Structure
```
src/
├── app.py              # Main Flask application with endpoints
├── seo_fetcher.py      # SEO data simulation module
├── ai_generator.py     # OpenAI integration for content generation
└── posts/              # Generated blog posts storage
```

### Dependencies & Libraries
- **Flask**: Web framework for REST API endpoints
- **OpenAI**: GPT model integration for content generation
- **APScheduler**: Background job scheduling for automation
- **python-dotenv**: Environment variable management for API keys
- **JSON**: Native Python library for structured data output

### Environment Configuration
```bash
# Required in .env file
OPENAI_API_KEY=your_openai_api_key_here
```

## API Usage Examples

### 1. Interactive Web Request
```bash
curl "http://localhost:5000/generate?keyword=smart%20watches"
```

### 2. JSON Response Format
```json
{
  "keyword": "smart watches",
  "seo_data": {
    "search_volume": 85000,
    "keyword_difficulty": 45,
    "avg_cpc": 1.80
  },
  "blog_post": "# Smart Watches: The Future of Wearable Technology\n\n..."
}
```

### 3. HTML Response Format
```html
<!DOCTYPE html>
<html>
<head>
    <title>AI Blog Generator - smart watches</title>
</head>
<body>
    <h1>Generated Blog Post: smart watches</h1>
    
    <div>
        <h3>SEO Research Data</h3>
        <p><strong>Search Volume:</strong> 85,000</p>
        <p><strong>Keyword Difficulty:</strong> 45</p>
        <p><strong>Average CPC:</strong> $1.80</p>
    </div>
    
    <div>
        <h1>Smart Watches: The Future of Wearable Technology</h1>
        <p>Welcome to our comprehensive guide...</p>
        
        <h2>Why Smart Watches Are Trending (Search Volume: 85000)</h2>
        <p>Content about trending factors...</p>
        
        <h2>Challenges and Competition (Keyword Difficulty: 45)</h2>
        <p>Content about market challenges...</p>
        
        <h2>Top Product Recommendations</h2>
        <p>1. Premium Smart Watch - <a href="https://example-affiliate.com/product1?ref=dummy123">Check it out</a></p>
        <p>2. Best Value Option - <a href="https://example-affiliate.com/product2?ref=dummy456">View product</a></p>
        <p>3. Budget Choice - <a href="https://example-affiliate.com/product3?ref=dummy789">See details</a></p>
        
        <h2>Conclusion</h2>
        <p>Concluding thoughts and call to action...</p>
    </div>
    
    <div>
        <p><em>Generated on: 2025-06-02 14:30:15</em></p>
        <p><em>Keyword: smart watches</em></p>
    </div>
</body>
</html>
```

## Automation Features

### Daily Content Generation
- **Frequency**: Every 24 hours
- **Default Keyword**: "wireless earbuds" (configurable)
- **Output**: Timestamped JSON files in `posts/` directory
- **Logging**: Console output with generation timestamps

### Scheduler Configuration
```python
# Customizable settings in app.py
SCHEDULER_GENERATION_INTERVAL = 1        # Days between generations
SCHEDULER_GENERATION_KEYWORD = "wireless earbuds"  # Target keyword
```

## Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Run Application
```bash
cd src
python app.py
```

### 4. Test Endpoints
```bash
# Test manual generation
curl "http://localhost:5000/generate?keyword=test"
```

## File Output Examples

Generated content is automatically saved with descriptive filenames:
- Manual requests: `keyword_YYYYMMDD-HHMMSS.html`
- Scheduled jobs: `daily_report_keyword_YYYYMMDD-HHMMSS.html`

Each file contains the complete generation context: keyword, SEO metrics, and AI-generated content with processed affiliate links.

## Customization Options

- **SEO Data**: Add more keywords to the mock database in `seo_fetcher.py`
- **AI Model**: Change `MODEL` variable in `ai_generator.py` (gpt-4, gpt-3.5-turbo)
- **Scheduling**: Modify interval and keywords in `app.py` configuration
- **Content Structure**: Adjust prompts in `ai_generator.py` for different blog formats
- **Output Format**: Customize JSON structure in the generation endpoints

This implementation provides a complete, production-ready Flask application that demonstrates all the core concepts of automated SEO content generation with AI assistance.


## (Additional) Streamlit UI

To run the interactive Streamlit interface, run the following command from the root of the project in a separate terminal:

```bash
cd screen
streamlit run screen.py