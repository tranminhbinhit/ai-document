import os
from pathlib import Path
from database import insert_document, document_exists

# Import document parsers
try:
    import PyPDF2
    import docx
    import openpyxl
except ImportError:
    print("Warning: Document parsers not installed")
    PyPDF2 = None
    docx = None
    openpyxl = None


def read_file(path):
    """Đọc nội dung file dựa trên extension"""
    path = Path(path)
    extension = path.suffix.lower()
    
    try:
        if extension == '.pdf' and PyPDF2:
            return read_pdf(path)
        elif extension == '.docx' and docx:
            return read_docx(path)
        elif extension == '.xlsx' and openpyxl:
            return read_xlsx(path)
        elif extension in ['.txt', '.md', '.json', '.csv']:
            return read_text(path)
        else:
            return f"Unsupported file type: {extension}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def read_text(path):
    """Đọc file text"""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read_pdf(path):
    """Đọc file PDF"""
    text_content = []
    with open(path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
    return "\n".join(text_content)


def read_docx(path):
    """Đọc file DOCX"""
    doc = docx.Document(path)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs)


def read_xlsx(path):
    """Đọc file XLSX"""
    wb = openpyxl.load_workbook(path, read_only=True)
    sheet = wb.active
    data = []
    for row in sheet.iter_rows(values_only=True):
        row_data = [str(cell) if cell is not None else "" for cell in row]
        data.append(" | ".join(row_data))
    return "\n".join(data)


def create_summary(text):
    """Tạo summary đơn giản (lấy 200 ký tự đầu)"""
    text = text.strip()
    if len(text) <= 200:
        return text
    return text[:200] + "..."


def extract_keywords(text):
    """Extract keywords đơn giản (top 10 từ phổ biến)"""
    # Đơn giản hóa: lấy các từ dài hơn 4 ký tự
    words = text.lower().split()
    words = [w.strip('.,!?;:()[]{}') for w in words if len(w) > 4]
    
    # Đếm frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Lấy top 10
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    keywords = [word for word, freq in top_words]
    
    return ", ".join(keywords)


def process_file(path):
    """Xử lý file mới hoặc đã thay đổi"""
    path = Path(path)
    
    # Bỏ qua các file tạm
    if path.name.startswith('~') or path.name.startswith('.'):
        return
    
    if document_exists(str(path)):
        print(f"Already indexed: {path.name}")
        return
    
    print(f"Processing: {path.name}")
    
    # Đọc và phân tích file
    text = read_file(path)
    summary = create_summary(text)
    keywords = extract_keywords(text)
    
    # Lưu vào database
    insert_document(
        file_name=path.name,
        path=str(path),
        summary=summary,
        keywords=keywords
    )
    
    print(f"✓ Indexed: {path.name}")