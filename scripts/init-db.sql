-- Create DocumentRAG database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'DocumentRAG')
BEGIN
    CREATE DATABASE DocumentRAG;
    PRINT 'Database DocumentRAG created successfully';
END
ELSE
BEGIN
    PRINT 'Database DocumentRAG already exists';
END
GO

USE DocumentRAG;
GO

-- Create tables if they don't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Categories]') AND type in (N'U'))
BEGIN
    CREATE TABLE [Categories] (
        [Id] INT PRIMARY KEY IDENTITY(1,1),
        [Name] NVARCHAR(200) NOT NULL,
        [Description] NVARCHAR(1000) NULL,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [UpdatedAt] DATETIME2 NULL
    );
    PRINT 'Table Categories created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Documents]') AND type in (N'U'))
BEGIN
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
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ChatSessions]') AND type in (N'U'))
BEGIN
    CREATE TABLE [ChatSessions] (
        [Id] INT PRIMARY KEY IDENTITY(1,1),
        [SessionId] UNIQUEIDENTIFIER NOT NULL UNIQUE,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE()
    );
    PRINT 'Table ChatSessions created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ChatMessages]') AND type in (N'U'))
BEGIN
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
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DocumentChunks]') AND type in (N'U'))
BEGIN
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
END
GO

-- Create indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Documents_CategoryId')
BEGIN
    CREATE INDEX [IX_Documents_CategoryId] ON [Documents]([CategoryId]);
    PRINT 'Index IX_Documents_CategoryId created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Documents_Status')
BEGIN
    CREATE INDEX [IX_Documents_Status] ON [Documents]([Status]);
    PRINT 'Index IX_Documents_Status created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ChatMessages_SessionId')
BEGIN
    CREATE INDEX [IX_ChatMessages_SessionId] ON [ChatMessages]([SessionId]);
    PRINT 'Index IX_ChatMessages_SessionId created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_DocumentChunks_DocumentId')
BEGIN
    CREATE INDEX [IX_DocumentChunks_DocumentId] ON [DocumentChunks]([DocumentId]);
    PRINT 'Index IX_DocumentChunks_DocumentId created';
END
GO

PRINT 'Database initialization completed successfully';
