"""
Intercom API service wrapper for help center management.
"""

import requests
import json
import logging
from typing import Optional, Dict, List, Union
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class IntercomService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.intercom.io"
        self.admin_id = "6409529"  # Sim's admin ID
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Intercom-Version": "2.13"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Intercom API with error handling"""
        try:
            # Handle both URL string and dict endpoints
            if isinstance(endpoint, str):
                url = f"{self.base_url}/{endpoint.lstrip('/')}"
            else:
                url = endpoint.get('url', '')
            
            # Log request details for debugging
            logger.debug(f"Making {method} request to {url}")
            if data:
                logger.debug(f"Request data: {json.dumps(data, indent=2)}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data if data else None,
                params=params if params else None
            )
            
            # Log response for debugging
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Intercom API error: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response body: {e.response.text}")
            raise

    def get_conversations(self, days_back: int = 30, tag: Optional[str] = None) -> List[Dict]:
        """
        Fetch conversations from the last N days.
        Optionally filter by tag.
        """
        try:
            start_date = datetime.now() - timedelta(days=days_back)
            params = {
                "created_at_after": int(start_date.timestamp()),
                "per_page": 50  # Adjust as needed
            }
            if tag:
                params["tag_id"] = tag

            conversations = []
            response = self._make_request("GET", "/conversations", params=params)
            conversations.extend(response.get('conversations', []))

            # Handle pagination
            while 'pages' in response and response['pages'].get('next'):
                next_page = response['pages']['next']
                response = self._make_request("GET", {"url": next_page})
                conversations.extend(response.get('conversations', []))

            return conversations
        except Exception as e:
            logger.error(f"Error fetching conversations: {e}")
            return []

    def get_conversation_details(self, conversation_id: str) -> Dict:
        """Fetch full conversation details including all messages"""
        try:
            return self._make_request("GET", f"/conversations/{conversation_id}")
        except Exception as e:
            logger.error(f"Error fetching conversation details: {e}")
            return {}

    def get_conversation_tags(self) -> List[Dict]:
        """Fetch all available conversation tags"""
        try:
            response = self._make_request("GET", "/tags")
            return response.get('data', [])
        except Exception as e:
            logger.error(f"Error fetching tags: {e}")
            return []

    def search_conversations(self, query: str) -> List[Dict]:
        """Search conversations by content"""
        try:
            params = {"q": query}
            response = self._make_request("GET", "/conversations/search", params=params)
            return response.get('conversations', [])
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            return []

    def get_all_articles(self) -> List[Dict]:
        """Retrieve all help center articles"""
        try:
            response = self._make_request("GET", "/articles")
            return response.get('data', [])
        except Exception as e:
            logger.error(f"Error getting articles: {e}")
            return []
    
    def create_article(self, title: str, body: str, author_id: Optional[str] = None, state: str = "draft", collection_id: Optional[str] = None) -> Dict:
        """Create new help article"""
        try:
            data = {
                "title": title,
                "body": body,
                "author_id": author_id or self.admin_id,
                "state": state,
                "type": "article"
            }
            
            if collection_id:
                data["parent_id"] = collection_id
                
            return self._make_request("POST", "/articles", data)
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            raise
    
    def update_article(self, article_id: str, title: Optional[str] = None, 
                      body: Optional[str] = None, state: Optional[str] = None,
                      collection_id: Optional[str] = None) -> Dict:
        """Update existing article"""
        try:
            data = {
                "author_id": self.admin_id
            }
            if title:
                data["title"] = title
            if body:
                data["body"] = body
            if state:
                data["state"] = state
            if collection_id:
                data["parent_id"] = collection_id
            
            return self._make_request("PUT", f"/articles/{article_id}", data)
        except Exception as e:
            logger.error(f"Error updating article: {e}")
            raise

    def move_to_collection(self, article_id: str, collection_id: str) -> Dict:
        """Move an article to a specific collection"""
        try:
            data = {
                "parent_id": collection_id,
                "author_id": self.admin_id
            }
            return self._make_request("PUT", f"/articles/{article_id}", data)
        except Exception as e:
            logger.error(f"Error moving article: {e}")
            raise
    
    def search_articles(self, query: str) -> List[Dict]:
        """Search for articles by title/content"""
        try:
            response = self._make_request("GET", "/articles/search", params={"q": query})
            return response.get('data', [])
        except Exception as e:
            logger.error(f"Error searching articles: {e}")
            return []
    
    def get_article_by_id(self, article_id: str) -> Dict:
        """Get article by ID"""
        try:
            return self._make_request("GET", f"/articles/{article_id}")
        except Exception as e:
            logger.error(f"Error getting article: {e}")
            raise
    
    def archive_article(self, article_id: str) -> Dict:
        """Archive an article"""
        return self.update_article(article_id, state="archived")
    
    def publish_article(self, article_id: str) -> Dict:
        """Publish an article"""
        return self.update_article(article_id, state="published")