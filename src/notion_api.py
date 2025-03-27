#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion API Integration Module with Token Optimization
----------------------------------------------------
This module provides functions to interact with Notion API
with optimized token usage for LLM context.
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union

# In a real implementation, you would use the Notion API client library
# For demonstration purposes, we're showing the structure
try:
    import requests
except ImportError:
    print("Requests library not installed. Run: pip install requests")


class NotionCache:
    """Cache manager for Notion data to reduce API calls and token usage"""
    
    def __init__(self, cache_dir: str = '.notion_cache'):
        """Initialize the Notion Cache
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, page_id: str) -> str:
        """Get the cache file path for a page ID
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Path to the cache file
        """
        return os.path.join(self.cache_dir, f"{page_id}.json")
    
    def get_cached_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get cached page content if available and not expired
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Cached page content or None if not available
        """
        cache_path = self.get_cache_path(page_id)
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                
                # Check if cache is still valid (24 hours)
                last_updated = datetime.fromisoformat(cached_data.get('cached_at', '2000-01-01'))
                if datetime.now() - last_updated < timedelta(hours=24):
                    return cached_data.get('content')
        return None
    
    def update_cache(self, page_id: str, content: Dict[str, Any]) -> None:
        """Update the cache for a page
        
        Args:
            page_id: Notion page ID
            content: Page content to cache
        """
        cache_path = self.get_cache_path(page_id)
        cache_data = {
            'content': content,
            'cached_at': datetime.now().isoformat()
        }
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f)
    
    def get_page_content(self, page_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Get page content from cache or fetch from API
        
        Args:
            page_id: Notion page ID
            force_refresh: Whether to force refresh from API
            
        Returns:
            Page content
        """
        if not force_refresh:
            cached_content = self.get_cached_page(page_id)
            if cached_content:
                return cached_content
        
        # Cache miss or force refresh, return None to indicate need for API call
        return None


class NotionManager:
    """Manager class for Notion operations with token optimization"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize the Notion Manager
        
        Args:
            token: Notion API token
        """
        self.token = token or os.environ.get('NOTION_TOKEN')
        if not self.token:
            raise ValueError("Notion token is required")
            
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
            
        self.base_url = 'https://api.notion.com/v1'
        self.cache = NotionCache()
        
    def get_page(self, page_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Get a Notion page by ID
        
        Args:
            page_id: Notion page ID
            force_refresh: Whether to force refresh from API
            
        Returns:
            Page data
        """
        # Try to get from cache first
        cached_page = self.cache.get_page_content(page_id, force_refresh)
        if cached_page and not force_refresh:
            return cached_page
        
        # Cache miss or force refresh, fetch from API
        url = f"{self.base_url}/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        page_data = response.json()
        
        # Update cache
        self.cache.update_cache(page_id, page_data)
        
        return page_data
    
    def get_block_children(self, block_id: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Get children blocks of a block
        
        Args:
            block_id: Block ID (can be a page ID)
            force_refresh: Whether to force refresh from API
            
        Returns:
            List of child blocks
        """
        # Try to get from cache first
        cache_key = f"{block_id}_children"
        cached_blocks = self.cache.get_page_content(cache_key, force_refresh)
        if cached_blocks and not force_refresh:
            return cached_blocks
        
        # Cache miss or force refresh, fetch from API
        url = f"{self.base_url}/blocks/{block_id}/children"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        blocks_data = response.json().get('results', [])
        
        # Update cache
        self.cache.update_cache(cache_key, blocks_data)
        
        return blocks_data
    
    def search_pages(self, query: str = "", filter_by: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for pages in Notion
        
        Args:
            query: Search query
            filter_by: Filter criteria
            
        Returns:
            List of matching pages
        """
        url = f"{self.base_url}/search"
        data = {"query": query}
        
        if filter_by:
            data["filter"] = filter_by
            
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json().get('results', [])
    
    def extract_plain_text(self, rich_text: List[Dict[str, Any]]) -> str:
        """Extract plain text from Notion rich text format
        
        Args:
            rich_text: Notion rich text array
            
        Returns:
            Plain text string
        """
        if not rich_text:
            return ""
            
        return "".join([text.get('plain_text', '') for text in rich_text])
    
    def simplify_block_content(self, block: Dict[str, Any]) -> Dict[str, str]:
        """Simplify a block to extract just the text content
        
        Args:
            block: Notion block
            
        Returns:
            Simplified block with type and content
        """
        block_type = block.get('type')
        simplified = {
            'type': block_type,
            'content': ''
        }
        
        if block_type == 'paragraph':
            simplified['content'] = self.extract_plain_text(block.get('paragraph', {}).get('rich_text', []))
        elif block_type == 'heading_1':
            simplified['content'] = self.extract_plain_text(block.get('heading_1', {}).get('rich_text', []))
        elif block_type == 'heading_2':
            simplified['content'] = self.extract_plain_text(block.get('heading_2', {}).get('rich_text', []))
        elif block_type == 'heading_3':
            simplified['content'] = self.extract_plain_text(block.get('heading_3', {}).get('rich_text', []))
        elif block_type == 'bulleted_list_item':
            simplified['content'] = self.extract_plain_text(block.get('bulleted_list_item', {}).get('rich_text', []))
        elif block_type == 'numbered_list_item':
            simplified['content'] = self.extract_plain_text(block.get('numbered_list_item', {}).get('rich_text', []))
        elif block_type == 'to_do':
            simplified['content'] = self.extract_plain_text(block.get('to_do', {}).get('rich_text', []))
            simplified['checked'] = block.get('to_do', {}).get('checked', False)
        elif block_type == 'toggle':
            simplified['content'] = self.extract_plain_text(block.get('toggle', {}).get('rich_text', []))
        elif block_type == 'code':
            simplified['content'] = self.extract_plain_text(block.get('code', {}).get('rich_text', []))
            simplified['language'] = block.get('code', {}).get('language', '')
        
        return simplified
    
    def get_page_content_simplified(self, page_id: str, max_blocks: int = 50) -> Dict[str, Any]:
        """Get simplified page content with reduced token usage
        
        Args:
            page_id: Notion page ID
            max_blocks: Maximum number of blocks to retrieve
            
        Returns:
            Simplified page content
        """
        # Get page metadata
        page = self.get_page(page_id)
        
        # Get page title
        title = ""
        properties = page.get('properties', {})
        for prop in properties.values():
            if prop.get('type') == 'title':
                title = self.extract_plain_text(prop.get('title', []))
                break
        
        # Get page blocks
        blocks = self.get_block_children(page_id)
        
        # Simplify blocks to reduce token usage
        simplified_blocks = []
        for i, block in enumerate(blocks):
            if i >= max_blocks:
                break
                
            simplified_blocks.append(self.simplify_block_content(block))
        
        return {
            'id': page_id,
            'title': title,
            'url': page.get('url', ''),
            'last_edited': page.get('last_edited_time', ''),
            'created': page.get('created_time', ''),
            'blocks': simplified_blocks
        }
    
    def generate_page_summary(self, page_id: str, max_length: int = 500) -> str:
        """Generate a summary of a page
        
        Args:
            page_id: Notion page ID
            max_length: Maximum length of summary in characters
            
        Returns:
            Page summary
        """
        # Get simplified page content
        content = self.get_page_content_simplified(page_id)
        
        # Extract text from blocks
        text_blocks = []
        for block in content.get('blocks', []):
            if block.get('content'):
                text_blocks.append(block.get('content'))
        
        # Join blocks into a single text
        full_text = "\n".join(text_blocks)
        
        # Simple summarization: truncate to max_length
        if len(full_text) <= max_length:
            return full_text
        
        # More sophisticated approach: take first paragraph and important sentences
        paragraphs = full_text.split('\n')
        summary = paragraphs[0] if paragraphs else ""
        
        # Add important sentences containing keywords
        keywords = ["important", "key", "main", "critical", "essential", "conclusion"]
        for paragraph in paragraphs[1:]:
            if len(summary) >= max_length:
                break
                
            # Check if paragraph contains any keywords
            if any(keyword in paragraph.lower() for keyword in keywords):
                if len(summary) + len(paragraph) + 1 <= max_length:
                    summary += "\n" + paragraph
        
        # If still under max_length, add more paragraphs
        i = 1
        while i < len(paragraphs) and len(summary) + len(paragraphs[i]) + 1 <= max_length:
            if paragraphs[i] not in summary:
                summary += "\n" + paragraphs[i]
            i += 1
        
        return summary
    
    def create_notion_page_index(self, database_id: str = None) -> Dict[str, Dict[str, Any]]:
        """Create an index of Notion pages for efficient access
        
        Args:
            database_id: Optional database ID to filter pages
            
        Returns:
            Dictionary of page IDs to page metadata
        """
        # Search for pages
        if database_id:
            filter_by = {"property": "object", "value": "page"}
            pages = self.search_pages(filter_by=filter_by)
        else:
            pages = self.search_pages()
        
        # Create index
        index = {}
        for page in pages:
            page_id = page.get('id')
            
            # Extract title
            title = ""
            properties = page.get('properties', {})
            for prop in properties.values():
                if prop.get('type') == 'title':
                    title = self.extract_plain_text(prop.get('title', []))
                    break
            
            # Extract tags/keywords if available
            tags = []
            for prop_name, prop in properties.items():
                if prop.get('type') == 'multi_select':
                    tags = [option.get('name', '') for option in prop.get('multi_select', [])]
                    break
            
            # Store in index
            index[page_id] = {
                'title': title,
                'url': page.get('url', ''),
                'last_edited': page.get('last_edited_time', ''),
                'created': page.get('created_time', ''),
                'tags': tags
            }
        
        return index
    
    def get_recently_updated_pages(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get pages updated in the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of recently updated pages
        """
        # Get all pages
        pages = self.search_pages()
        
        # Filter by last edited time
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        recent_pages = []
        
        for page in pages:
            last_edited = page.get('last_edited_time', '')
            if last_edited >= cutoff_date:
                # Extract title
                title = ""
                properties = page.get('properties', {})
                for prop in properties.values():
                    if prop.get('type') == 'title':
                        title = self.extract_plain_text(prop.get('title', []))
                        break
                
                recent_pages.append({
                    'id': page.get('id'),
                    'title': title,
                    'url': page.get('url', ''),
                    'last_edited': last_edited
                })
        
        # Sort by last edited time (most recent first)
        recent_pages.sort(key=lambda x: x.get('last_edited', ''), reverse=True)
        
        return recent_pages


def main():
    """Example usage of the NotionManager class"""
    # Use Notion token from environment variable
    try:
        notion = NotionManager()
        
        # Example: Search for pages
        print("Searching for pages...")
        pages = notion.search_pages()
        print(f"Found {len(pages)} pages")
        
        if pages:
            # Get the first page ID
            page_id = pages[0].get('id')
            
            # Get simplified page content
            print(f"\nGetting simplified content for page {page_id}...")
            content = notion.get_page_content_simplified(page_id)
            
            print(f"Page title: {content.get('title')}")
            print(f"Number of blocks: {len(content.get('blocks', []))}")
            
            # Generate summary
            print("\nGenerating page summary...")
            summary = notion.generate_page_summary(page_id)
            print(f"Summary ({len(summary)} chars):")
            print(summary[:200] + "..." if len(summary) > 200 else summary)
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
