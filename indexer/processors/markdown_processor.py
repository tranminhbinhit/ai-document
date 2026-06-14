import logging
import markdown
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_text_from_markdown(file_path: str) -> str:
    """Extract text from Markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html = markdown.markdown(md_content)
        
        # Extract text from HTML
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from Markdown: {e}")
        raise
