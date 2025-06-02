# seo_fetcher.py

def fetch_seo_data(keyword):
    mock_database = {
        "wireless earbuds": {
            "search_volume": 120000,
            "keyword_difficulty": 37,
            "avg_cpc": 1.25
        },
        "standing desk": {
            "search_volume": 90000,
            "keyword_difficulty": 42,
            "avg_cpc": 2.10
        },
        "ai blog generator": {
            "search_volume": 1200,
            "keyword_difficulty": 28,
            "avg_cpc": 0.75
        }
    }

    default_metrics = {
        "search_volume": 1000,
        "keyword_difficulty": 35,
        "avg_cpc": 0.50
    }

    return mock_database.get(keyword.lower(), default_metrics)
