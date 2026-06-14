-- Tạo database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DocumentAI')
BEGIN
    CREATE DATABASE DocumentAI;
END
GO

USE DocumentAI;
GO

-- Tạo bảng Documents
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Documents')
BEGIN
    CREATE TABLE Documents (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        FileName NVARCHAR(255) NOT NULL,
        Path NVARCHAR(500) NOT NULL UNIQUE,
        Summary NVARCHAR(MAX),
        Keywords NVARCHAR(MAX),
        IsDelete BIT DEFAULT 0,
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME DEFAULT GETDATE()
    );
    
    -- Index cho tìm kiếm nhanh
    CREATE INDEX IX_Documents_Path ON Documents(Path);
    CREATE INDEX IX_Documents_Keywords ON Documents(Keywords);
    CREATE INDEX IX_Documents_IsDelete ON Documents(IsDelete);
END
GO

-- Sample data (optional)
-- INSERT INTO Documents (FileName, Path, Summary, Keywords) 
-- VALUES ('sample.pdf', '/documents/sample.pdf', 'Sample document', 'sample,test,document');
GO
