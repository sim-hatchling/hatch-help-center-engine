"""
Fetch and save the latest articles from Intercom.
"""
import json
import os
from services.intercom_service import IntercomService
from config import Config

def main():
    # Initialize Intercom service
    intercom = IntercomService(Config.INTERCOM_ACCESS_TOKEN)
    
    # Create directory if it doesn't exist
    os.makedirs('latest_articles', exist_ok=True)
    
    print("Fetching articles from Intercom...")
    articles = intercom.get_all_articles()
    
    # Save each article
    for article in articles:
        if article.get('state') == 'published':
            filename = f"latest_articles/{article['id']}.json"
            with open(filename, 'w') as f:
                json.dump(article, f, indent=2)
            print(f"Saved article: {article.get('title', 'Untitled')}")
    
    print("\nAll articles saved!")

if __name__ == "__main__":
    main()
