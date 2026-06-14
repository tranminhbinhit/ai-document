import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_text_from_html(file_path: str) -> str:
    """Extract text from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from HTML: {e}")
        raise
