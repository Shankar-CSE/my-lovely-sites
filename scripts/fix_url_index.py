#!/usr/bin/env python3
"""
Fix the URL index to be sparse to support collections
Usage: python scripts/fix_url_index.py
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def fix_index():
    """Drop the old unique index and recreate as sparse"""
    print("=" * 50)
    print("Fix URL Index for Collections Support")
    print("=" * 50)
    print()
    
    try:
        # Connect directly to avoid index creation
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/url_organizer')
        client = MongoClient(mongo_uri)
        
        # Extract database name from URI or use default
        db_name = mongo_uri.split('/')[-1].split('?')[0] or 'url_organizer'
        db = client[db_name]
        urls_collection = db.urls
        
        # Get existing indexes
        print("📋 Current indexes:")
        indexes = urls_collection.index_information()
        for idx_name, idx_info in indexes.items():
            print(f"  • {idx_name}: {idx_info}")
        print()
        
        # Drop the old url_1 index if it exists and is not sparse
        if 'url_1' in indexes:
            idx_info = indexes['url_1']
            if not idx_info.get('sparse', False):
                print("🔧 Dropping old 'url_1' index (non-sparse)...")
                urls_collection.drop_index('url_1')
                print("  ✓ Old index dropped")
                
                # Create new sparse unique index
                print("\n🔧 Creating new sparse unique index on 'url'...")
                urls_collection.create_index([('url', 1)], unique=True, sparse=True)
                print("  ✓ New sparse index created")
            else:
                print("ℹ️  Index 'url_1' is already sparse - no changes needed")
        else:
            print("ℹ️  No 'url_1' index found")
            print("\n🔧 Creating new sparse unique index on 'url'...")
            urls_collection.create_index([('url', 1)], unique=True, sparse=True)
            print("  ✓ New sparse index created")
        
        # Show updated indexes
        print("\n📋 Updated indexes:")
        indexes = urls_collection.index_information()
        for idx_name, idx_info in indexes.items():
            print(f"  • {idx_name}: {idx_info}")
        
        print("\n" + "=" * 50)
        print("✅ Index fix complete!")
        print("=" * 50)
        print("\nYou can now create URL collections successfully.")
        print()
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    try:
        fix_index()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
