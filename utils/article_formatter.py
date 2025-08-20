"""
Utility functions for formatting Intercom articles.
"""
from bs4 import BeautifulSoup
import markdown2
import re

def format_content(content: str, add_title: bool = False, title: str = None) -> str:
    """
    Format article content with proper HTML and Intercom classes.
    
    Args:
        content: Markdown or HTML content
        add_title: Whether to add the title as H1
        title: Article title (required if add_title is True)
    """
    # Convert markdown to HTML
    html = markdown2.markdown(content, extras=['tables'])
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Add title if requested
    if add_title and title:
        h1 = soup.new_tag('h1')
        h1.string = title
        soup.insert(0, h1)
    
    # Add Intercom classes
    for p in soup.find_all('p'):
        p['class'] = 'no-margin'
    
    # Add table classes
    for table in soup.find_all('table'):
        table.wrap(soup.new_tag('div', attrs={'class': 'intercom-interblocks-table-container'}))
        table['role'] = 'presentation'
    
    return str(soup)

def clean_html(content: str) -> str:
    """
    Clean HTML content by removing extra whitespace and formatting.
    """
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove the first h1 (title) if it exists
    if first_h1 := soup.find('h1'):
        first_h1.decompose()
    
    # Get the clean content
    content = str(soup)
    
    # Remove extra line breaks at the start
    content = re.sub(r'^\s+', '', content)
    
    return content
