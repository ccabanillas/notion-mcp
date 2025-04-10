"""Pydantic models for Notion API objects."""

from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class NotionObject(BaseModel):
    """Base class for Notion objects."""
    model_config = ConfigDict(extra="ignore")
    
    object: str
    id: str
    created_time: datetime
    last_edited_time: Optional[datetime] = None
    url: Optional[str] = None
    public_url: Optional[str] = None

class RichText(BaseModel):
    """Model for rich text content."""
    model_config = ConfigDict(extra="ignore")
    
    type: str
    text: Dict[str, Any] = Field(default_factory=dict)
    annotations: Optional[Dict[str, Any]] = None
    plain_text: Optional[str] = None
    href: Optional[str] = None

class PropertyValue(BaseModel):
    """Model for property values."""
    model_config = ConfigDict(extra="ignore")
    
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
    email: Optional[str] = None
    phone_number: Optional[str] = None
    formula: Optional[Dict[str, Any]] = None
    relation: Optional[List[Dict[str, str]]] = None
    rollup: Optional[Dict[str, Any]] = None
    created_time: Optional[datetime] = None
    created_by: Optional[Dict[str, Any]] = None
    last_edited_time: Optional[datetime] = None
    last_edited_by: Optional[Dict[str, Any]] = None
    files: Optional[List[Dict[str, Any]]] = None
    status: Optional[Dict[str, Any]] = None

class Page(NotionObject):
    """Model for a Notion page."""
    parent: Dict[str, Any]
    archived: bool = False
    properties: Dict[str, Any]
    
    def model_post_init(self, __context):
        """Process properties after initialization"""
        processed_properties = {}
        for key, value in self.properties.items():
            if isinstance(value, dict) and 'type' in value:
                try:
                    processed_properties[key] = PropertyValue.model_validate(value)
                except Exception:
                    # Keep the original value if validation fails
                    processed_properties[key] = value
            else:
                processed_properties[key] = value
        self.properties = processed_properties

class DatabaseProperty(BaseModel):
    """Model for database property configuration."""
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    type: str
    
    # Type-specific configurations
    number: Optional[Dict[str, Any]] = None
    select: Optional[Dict[str, Any]] = None
    multi_select: Optional[Dict[str, Any]] = None
    status: Optional[Dict[str, Any]] = None
    formula: Optional[Dict[str, Any]] = None
    relation: Optional[Dict[str, Any]] = None
    rollup: Optional[Dict[str, Any]] = None

class Database(NotionObject):
    """Model for a Notion database."""
    title: List[RichText]
    description: List[RichText] = Field(default_factory=list)
    properties: Dict[str, Any]
    archived: bool = False
    
    def model_post_init(self, __context):
        """Process properties after initialization"""
        processed_properties = {}
        for key, value in self.properties.items():
            if isinstance(value, dict) and 'type' in value:
                try:
                    processed_properties[key] = DatabaseProperty.model_validate(value)
                except Exception:
                    # Keep the original value if validation fails
                    processed_properties[key] = value
            else:
                processed_properties[key] = value
        self.properties = processed_properties

class Block(NotionObject):
    """Model for a Notion block."""
    type: str
    has_children: bool = False
    archived: bool = False
    content: Dict[str, Any] = Field(default_factory=dict)
    
    def model_post_init(self, __context):
        """Process block content based on type"""
        if self.type in self.__dict__ and isinstance(self.__dict__[self.type], dict):
            self.content = self.__dict__[self.type]

class SearchResults(BaseModel):
    """Model for search results."""
    model_config = ConfigDict(extra="ignore")
    
    object: str = "list"
    results: List[Any]
    next_cursor: Optional[str] = None
    has_more: bool = False 