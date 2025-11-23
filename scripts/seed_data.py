#!/usr/bin/env python3
"""
Seed sample data into the URL organizer database
Usage: python scripts/seed_data.py
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_db
from datetime import datetime, timedelta
import random


SAMPLE_URLS = [
    {
        "title": "Python Official Documentation",
        "url": "https://docs.python.org/3/",
        "description": "The official Python documentation with tutorials, library reference, and language reference.",
        "tags": ["python", "documentation", "programming"]
    },
    {
        "title": "Flask Web Framework",
        "url": "https://flask.palletsprojects.com/",
        "description": "Flask is a lightweight WSGI web application framework for Python.",
        "tags": ["python", "flask", "web", "framework"]
    },
    {
        "title": "MongoDB Documentation",
        "url": "https://www.mongodb.com/docs/",
        "description": "Official MongoDB documentation including guides, tutorials, and API reference.",
        "tags": ["database", "mongodb", "nosql", "documentation"]
    },
    {
        "title": "Tailwind CSS",
        "url": "https://tailwindcss.com/",
        "description": "A utility-first CSS framework for rapidly building custom user interfaces.",
        "tags": ["css", "tailwind", "frontend", "design"]
    },
    {
        "title": "GitHub",
        "url": "https://github.com/",
        "description": "GitHub is where over 100 million developers shape the future of software, together.",
        "tags": ["git", "github", "development", "collaboration"]
    },
    {
        "title": "Stack Overflow",
        "url": "https://stackoverflow.com/",
        "description": "Stack Overflow is the largest online community for programmers to learn and share knowledge.",
        "tags": ["community", "programming", "q&a", "help"]
    },
    {
        "title": "MDN Web Docs",
        "url": "https://developer.mozilla.org/",
        "description": "Resources for developers, by developers. Comprehensive documentation for web technologies.",
        "tags": ["web", "html", "css", "javascript", "documentation"]
    },
    {
        "title": "Real Python",
        "url": "https://realpython.com/",
        "description": "Learn Python online with tutorials, courses, and resources for all skill levels.",
        "tags": ["python", "tutorial", "learning", "programming"]
    },
    {
        "title": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/",
        "description": "Learn to code for free with interactive lessons and build projects.",
        "tags": ["learning", "tutorial", "web", "programming", "free"]
    },
    {
        "title": "Dev.to Community",
        "url": "https://dev.to/",
        "description": "A constructive and inclusive social network for software developers.",
        "tags": ["community", "blog", "programming", "articles"]
    },
    {
        "title": "PyPI - Python Package Index",
        "url": "https://pypi.org/",
        "description": "Find, install and publish Python packages with the Python Package Index.",
        "tags": ["python", "packages", "library", "tools"]
    },
    {
        "title": "VS Code",
        "url": "https://code.visualstudio.com/",
        "description": "Visual Studio Code is a lightweight but powerful source code editor.",
        "tags": ["editor", "ide", "development", "tools"]
    },
    {
        "title": "Regex101",
        "url": "https://regex101.com/",
        "description": "Online regex tester and debugger with highlighting for different languages.",
        "tags": ["regex", "tools", "testing", "development"]
    },
    {
        "title": "Can I Use",
        "url": "https://caniuse.com/",
        "description": "Browser support tables for modern web technologies.",
        "tags": ["web", "compatibility", "browser", "tools"]
    },
    {
        "title": "JSON Placeholder",
        "url": "https://jsonplaceholder.typicode.com/",
        "description": "Free fake API for testing and prototyping.",
        "tags": ["api", "testing", "development", "tools"]
    }
]


def seed_database():
    """Seed the database with sample URL data"""
    print("=" * 50)
    print("URL Organizer - Database Seeder")
    print("=" * 50)
    print()
    
    try:
        # Get database connection
        db = get_db()
        urls_collection = db.urls
        
        # Check if data already exists
        existing_count = urls_collection.count_documents({})
        if existing_count > 0:
            response = input(f"\n⚠️  Database already contains {existing_count} URLs. Continue? (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled.")
                return
        
        # Insert sample data
        print(f"\n📝 Adding {len(SAMPLE_URLS)} sample URLs...")
        
        inserted_count = 0
        skipped_count = 0
        
        for i, url_data in enumerate(SAMPLE_URLS, 1):
            # Add timestamps with some variation
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            url_data['created_at'] = created_at
            url_data['updated_at'] = created_at
            
            try:
                urls_collection.insert_one(url_data)
                print(f"  ✓ [{i}/{len(SAMPLE_URLS)}] {url_data['title']}")
                inserted_count += 1
            except Exception as e:
                print(f"  ✗ [{i}/{len(SAMPLE_URLS)}] {url_data['title']} (already exists)")
                skipped_count += 1
        
        # Show results
        print("\n" + "=" * 50)
        print("✓ Seeding complete!")
        print("=" * 50)
        print(f"  • Inserted: {inserted_count}")
        print(f"  • Skipped: {skipped_count}")
        print(f"  • Total URLs: {urls_collection.count_documents({})}")
        
        # Show tag statistics
        pipeline = [
            {'$unwind': '$tags'},
            {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]
        tag_stats = list(urls_collection.aggregate(pipeline))
        
        if tag_stats:
            print(f"  • Unique tags: {len(tag_stats)}")
            print("\n  Top tags:")
            for tag in tag_stats[:5]:
                print(f"    - {tag['_id']}: {tag['count']}")
        
        print("\n🚀 You can now run the application: python run.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        seed_database()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
