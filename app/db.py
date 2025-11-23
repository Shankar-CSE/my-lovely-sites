from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

_client = None
_db = None
_connection_attempted = False


def get_db():
    """Get database connection singleton (lazy initialization)"""
    global _client, _db, _connection_attempted
    
    if _db is not None:
        return _db
    
    if _connection_attempted and _db is None:
        # Already tried and failed, raise error
        raise ConnectionFailure("MongoDB connection not available. Check your MONGO_URI in .env file.")
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/url_organizer')
    _connection_attempted = True
    
    try:
        # Increase timeout for Atlas connections
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        # Test connection
        _client.admin.command('ping')
        
        # Extract database name from URI or use default
        db_name = mongo_uri.split('/')[-1].split('?')[0] or 'url_organizer'
        _db = _client[db_name]
        
        # Create indexes
        _ensure_indexes()
        
        print(f"✓ Connected to MongoDB: {db_name}")
        return _db
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check your MONGO_URI in .env file")
        print("   2. Ensure MongoDB Atlas cluster is running")
        print("   3. Verify network access (whitelist your IP in Atlas)")
        print("   4. Check username and password are correct\n")
        _db = None
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


def test_connection():
    """Test if database connection is available"""
    try:
        db = get_db()
        db.command('ping')
        return True
    except:
        return False


def close_db():
    """Close database connection"""
    global _client, _db, _connection_attempted
    if _client:
        _client.close()
        _client = None
        _db = None
        _connection_attempted = False
