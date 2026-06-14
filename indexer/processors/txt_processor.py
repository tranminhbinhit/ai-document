import logging

logger = logging.getLogger(__name__)

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            raise
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {e}")
        raise
