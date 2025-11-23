from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

_client = None
_db = None


def get_db():
    """Get database connection singleton"""
    global _client, _db
    
    if _db is not None:
        return _db
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/url_organizer')
    
    try:
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        _client.admin.command('ping')
        
        # Extract database name from URI or use default
        db_name = mongo_uri.split('/')[-1].split('?')[0] or 'url_organizer'
        _db = _client[db_name]
        
        # Create indexes
        _ensure_indexes()
        
        print(f"✓ Connected to MongoDB: {db_name}")
        return _db
        
    except ConnectionFailure as e:
        print(f"✗ MongoDB connection failed: {e}")
        raise


def _ensure_indexes():
    """Create necessary database indexes"""
    urls = _db.urls
    
    # Unique index on URL
    urls.create_index([('url', ASCENDING)], unique=True)
    
    # Text index for search
    urls.create_index([
        ('title', TEXT),
        ('description', TEXT)
    ], name='text_search')
    
    # Index for tag filtering
    urls.create_index([('tags', ASCENDING)])
    
    # Index for sorting by creation date
    urls.create_index([('created_at', ASCENDING)])


def close_db():
    """Close database connection"""
    global _client
    if _client:
        _client.close()
        _client = None
