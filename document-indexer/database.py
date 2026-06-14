import pyodbc
from config import DB_CONFIG


def get_connection():

    conn_string = f"""
    DRIVER={{{DB_CONFIG['driver']}}};
    SERVER={DB_CONFIG['server']};
    DATABASE={DB_CONFIG['database']};
    UID={DB_CONFIG['username']};
    PWD={DB_CONFIG['password']};
    TrustServerCertificate=yes;
    """

    return pyodbc.connect(conn_string)



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