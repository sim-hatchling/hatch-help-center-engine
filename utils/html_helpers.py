def create_section(title: str, content: str, level: int = 2) -> str:
    """
    Create an HTML section with a header.
    
    Args:
        title: Section title
        content: Section content
        level: Header level (2-6)
    """
    if not 2 <= level <= 6:
        level = 2
    return f'<h{level}>{title}</h{level}>\n\n{content}\n\n'

def create_list(items: list, ordered: bool = False) -> str:
    """
    Create an HTML list.
    
    Args:
        items: List of items
        ordered: If True, creates an ordered list (ol), otherwise unordered (ul)
    """
    tag = "ol" if ordered else "ul"
    items_html = "\n".join(f"  <li>{item}</li>" for item in items)
    return f'<{tag}>\n{items_html}\n</{tag}>'

def create_divider() -> str:
    """Create a horizontal divider."""
    return '<hr class="intercom-hr">\n\n'

def bold(text: str) -> str:
    """Wrap text in bold tags."""
    return f'<strong>{text}</strong>'

def italic(text: str) -> str:
    """Wrap text in italic tags."""
    return f'<em>{text}</em>'

def create_link(text: str, url: str, new_tab: bool = True) -> str:
    """
    Create an HTML link.
    
    Args:
        text: Link text
        url: URL to link to
        new_tab: Whether to open in new tab (default True)
    """
    target = ' target="_blank" rel="noopener noreferrer"' if new_tab else ''
    return f'<a href="{url}"{target}>{text}</a>'