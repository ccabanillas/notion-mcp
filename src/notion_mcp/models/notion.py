"""Pydantic models for Notion API objects."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class NotionObject(BaseModel):
    """Base class for Notion objects."""
    object: str
    id: str
    created_time: datetime
    last_edited_time: Optional[datetime] = None
    url: Optional[str] = None
    public_url: Optional[str] = None

class RichText(BaseModel):
    """Model for rich text content."""
    type: str
    text: Dict[str, Any]
    annotations: Optional[Dict[str, Any]] = None
    plain_text: Optional[str] = None
    href: Optional[str] = None

class PropertyValue(BaseModel):
    """Model for property values."""
    id: str
    type: str
    title: Optional[List[RichText]] = None
    rich_text: Optional[List[RichText]] = None
    select: Optional[Dict[str, Any]] = None
    multi_select: Optional[List[Dict[str, Any]]] = None
    url: Optional[str] = None
    checkbox: Optional[bool] = None
    number: Optional[float] = None
    date: Optional[Dict[str, Any]] = None

class Page(NotionObject):
    """Model for a Notion page."""
    parent: Dict[str, Any]
    archived: bool = False
    properties: Dict[str, PropertyValue]

class DatabaseProperty(BaseModel):
    """Model for database property configuration."""
    id: str
    name: str
    type: str

class Database(NotionObject):
    """Model for a Notion database."""
    title: List[RichText]
    description: List[RichText] = Field(default_factory=list)
    properties: Dict[str, DatabaseProperty]
    archived: bool = False

class SearchResults(BaseModel):
    """Model for search results."""
    object: str = "list"
    results: List[Union[Database, Page]]
    next_cursor: Optional[str] = None
    has_more: bool = False 