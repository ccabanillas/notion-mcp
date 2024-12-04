"""Notion API client implementation."""

import os
from typing import Any, Dict, List, Optional
import httpx
from .models.notion import Database, Page, SearchResults

class NotionClient:
    """Client for interacting with the Notion API."""
    
    def __init__(self, api_key: str):
        """Initialize the Notion client.
        
        Args:
            api_key: Notion API key
        """
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    async def list_databases(self) -> List[Database]:
        """List all databases the integration has access to."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={
                    "filter": {
                        "property": "object",
                        "value": "database"
                    },
                    "page_size": 100,
                    "sort": {
                        "direction": "descending",
                        "timestamp": "last_edited_time"
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("results"):
                return []
            return [Database(**db) for db in data["results"]]
    
    async def query_database(
        self,
        database_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Query a database."""
        body = {
            "page_size": page_size
        }
        if filter:
            body["filter"] = filter
        if sorts:
            body["sorts"] = sorts
        if start_cursor:
            body["start_cursor"] = start_cursor
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/databases/{database_id}/query",
                headers=self.headers,
                json=body
            )
            response.raise_for_status()
            return response.json()
    
    async def create_page(
        self,
        parent_id: str,
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None
    ) -> Page:
        """Create a new page."""
        body = {
            "parent": {"database_id": parent_id},
            "properties": properties
        }
        if children:
            body["children"] = children
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=body
            )
            response.raise_for_status()
            return Page(**response.json())
    
    async def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any],
        archived: Optional[bool] = None
    ) -> Page:
        """Update a page."""
        body = {"properties": properties}
        if archived is not None:
            body["archived"] = archived
            
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/pages/{page_id}",
                headers=self.headers,
                json=body
            )
            response.raise_for_status()
            return Page(**response.json())
    
    async def search(
        self,
        query: str = "",
        filter: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, Any]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> SearchResults:
        """Search Notion."""
        body = {
            "query": query,
            "page_size": page_size
        }
        if filter:
            body["filter"] = filter
        if sort:
            body["sort"] = sort
        if start_cursor:
            body["start_cursor"] = start_cursor
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json=body
            )
            response.raise_for_status()
            data = response.json()
            
            # Convert results based on their object type
            results = []
            for item in data.get("results", []):
                if item["object"] == "database":
                    results.append(Database(**item))
                elif item["object"] == "page":
                    # Convert property values to the correct format
                    properties = {}
                    for key, value in item.get("properties", {}).items():
                        properties[key] = PropertyValue(**value)
                    item["properties"] = properties
                    results.append(Page(**item))
            
            return SearchResults(
                object="list",
                results=results,
                next_cursor=data.get("next_cursor"),
                has_more=data.get("has_more", False)
            ) 