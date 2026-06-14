#!/usr/bin/env python3
"""
Integration test cho Document Indexer
Test workflow: File mới -> Process -> Database -> Query
"""

import os
import time
from pathlib import Path
from database import insert_document, document_exists, search_document, get_connection

def test_database_connection():
    """Test kết nối database"""
    print("Testing database connection...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        assert result[0] == 1
        print("✅ Database connection OK")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_insert_document():
    """Test insert document"""
    print("\nTesting document insert...")
    test_path = "/test/sample.pdf"
    
    try:
        insert_document(
            file_name="sample.pdf",
            path=test_path,
            summary="This is a test document for integration testing",
            keywords="test, sample, integration"
        )
        print("✅ Document inserted")
        return True
    except Exception as e:
        print(f"❌ Insert failed: {e}")
        return False


def test_document_exists():
    """Test kiểm tra document exists"""
    print("\nTesting document_exists...")
    test_path = "/test/sample.pdf"
    
    try:
        exists = document_exists(test_path)
        assert exists == True
        print("✅ Document exists check OK")
        return True
    except Exception as e:
        print(f"❌ Exists check failed: {e}")
        return False


def test_search_document():
    """Test search document"""
    print("\nTesting document search...")
    
    try:
        results = search_document("test")
        assert len(results) > 0
        print(f"✅ Search found {len(results)} documents")
        for row in results:
            print(f"   - {row[0]}: {row[2][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False


def test_cleanup():
    """Cleanup test data"""
    print("\nCleaning up test data...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Documents WHERE Path LIKE '/test/%'")
        conn.commit()
        conn.close()
        print("✅ Cleanup OK")
        return True
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Document Indexer Integration Test")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_insert_document,
        test_document_exists,
        test_search_document,
        test_cleanup
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
