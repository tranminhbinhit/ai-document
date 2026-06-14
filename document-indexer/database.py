import pymssql
from config import DB_CONFIG


def get_connection():
    """Tạo kết nối SQL Server sử dụng pymssql"""
    return pymssql.connect(
        server=DB_CONFIG['server'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['username'],
        password=DB_CONFIG['password']
    )



def insert_document(
        file_name,
        path,
        summary,
        keywords
):

    conn = get_connection()

    cursor = conn.cursor()


    sql = """
    INSERT INTO Documents
    (
        FileName,
        Path,
        Summary,
        Keywords,
        CreatedDate
    )
    VALUES
    (?, ?, ?, ?, GETDATE())
    """


    cursor.execute(
        sql,
        file_name,
        path,
        summary,
        keywords
    )


    conn.commit()

    cursor.close()
    conn.close()



def document_exists(path):

    conn = get_connection()

    cursor = conn.cursor()


    sql = """
    SELECT COUNT(*)
    FROM Documents
    WHERE Path = ?
    """


    cursor.execute(
        sql,
        path
    )


    count = cursor.fetchone()[0]


    cursor.close()
    conn.close()


    return count > 0



def search_document(keyword):

    conn = get_connection()

    cursor = conn.cursor()


    sql = """
    SELECT
        FileName,
        Path,
        Summary
    FROM Documents
    WHERE Keywords LIKE ?
    """


    cursor.execute(
        sql,
        f"%{keyword}%"
    )


    result = cursor.fetchall()


    conn.close()


    return result



def update_document(path, summary, keywords):
    """Update document metadata"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
    UPDATE Documents
    SET Summary = ?,
        Keywords = ?,
        ModifiedDate = GETDATE()
    WHERE Path = ?
    """
    
    cursor.execute(sql, summary, keywords, path)
    conn.commit()
    
    cursor.close()
    conn.close()