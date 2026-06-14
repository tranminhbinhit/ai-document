import os

DB_CONFIG = {
    "server": os.getenv("DB_SERVER", "localhost"),
    "database": os.getenv("DB_DATABASE", "DocumentAI"),
    "username": os.getenv("DB_USER", "sa"),
    "password": os.getenv("DB_PASSWORD", "YourStrong@Password123")
}