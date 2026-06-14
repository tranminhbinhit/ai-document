-- Drop and recreate DocumentRAG database completely
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'DocumentRAG')
BEGIN
    USE master;
    ALTER DATABASE DocumentRAG SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DocumentRAG;
    PRINT 'Database DocumentRAG dropped';
END
GO

-- Create DocumentRAG database
CREATE DATABASE DocumentRAG;
PRINT 'Database DocumentRAG created successfully';
GO

USE DocumentRAG;
GO

-- Create Categories table
CREATE TABLE [Categories] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [Name] NVARCHAR(200) NOT NULL,
    [Description] NVARCHAR(1000) NULL,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [UpdatedAt] DATETIME2 NULL
);
PRINT 'Table Categories created';
GO

-- Create Documents table
CREATE TABLE [Documents] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [Title] NVARCHAR(500) NOT NULL,
    [OriginalFileName] NVARCHAR(500) NOT NULL,
    [StorageFileName] NVARCHAR(500) NOT NULL,
    [FilePath] NVARCHAR(1000) NOT NULL,
    [FileSize] BIGINT NOT NULL,
    [FileType] NVARCHAR(50) NOT NULL,
    [CategoryId] INT NOT NULL,
    [Status] INT NOT NULL DEFAULT 0,
    [UploadedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [ProcessedAt] DATETIME2 NULL,
    [ErrorMessage] NVARCHAR(MAX) NULL,
    CONSTRAINT [FK_Documents_Categories] FOREIGN KEY ([CategoryId]) REFERENCES [Categories]([Id]) ON DELETE CASCADE
);
PRINT 'Table Documents created';
GO

-- Create ChatSessions table
CREATE TABLE [ChatSessions] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [SessionId] UNIQUEIDENTIFIER NOT NULL UNIQUE,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
PRINT 'Table ChatSessions created';
GO

-- Create ChatMessages table
CREATE TABLE [ChatMessages] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [SessionId] INT NOT NULL,
    [Role] NVARCHAR(50) NOT NULL,
    [Content] NVARCHAR(MAX) NOT NULL,
    [Sources] NVARCHAR(MAX) NULL,
    [ConfidenceScore] DECIMAL(5,4) NULL,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT [FK_ChatMessages_Sessions] FOREIGN KEY ([SessionId]) REFERENCES [ChatSessions]([Id]) ON DELETE CASCADE
);
PRINT 'Table ChatMessages created';
GO

-- Create DocumentChunks table
CREATE TABLE [DocumentChunks] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [DocumentId] INT NOT NULL,
    [ChunkText] NVARCHAR(MAX) NOT NULL,
    [ChunkIndex] INT NOT NULL,
    [Embedding] VARBINARY(MAX) NULL,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT [FK_DocumentChunks_Documents] FOREIGN KEY ([DocumentId]) REFERENCES [Documents]([Id]) ON DELETE CASCADE
);
PRINT 'Table DocumentChunks created';
GO

-- Create indexes
CREATE INDEX [IX_Documents_CategoryId] ON [Documents]([CategoryId]);
PRINT 'Index IX_Documents_CategoryId created';
GO

CREATE INDEX [IX_Documents_Status] ON [Documents]([Status]);
PRINT 'Index IX_Documents_Status created';
GO

CREATE INDEX [IX_ChatMessages_SessionId] ON [ChatMessages]([SessionId]);
PRINT 'Index IX_ChatMessages_SessionId created';
GO

CREATE INDEX [IX_DocumentChunks_DocumentId] ON [DocumentChunks]([DocumentId]);
PRINT 'Index IX_DocumentChunks_DocumentId created';
GO

-- Insert default categories
INSERT INTO [Categories] ([Name], [Description]) VALUES 
('General', 'General documents'),
('Technical', 'Technical documentation'),
('Business', 'Business documents'),
('Legal', 'Legal documents');
PRINT 'Default categories inserted';
GO

PRINT 'Database reset and initialization completed successfully';