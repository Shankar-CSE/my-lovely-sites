from app.db import get_db
from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError


class URLRepository:
    """Repository for URL database operations"""
    
    def __init__(self):
        self.collection = get_db().urls
    
    def create(self, url_data):
        """Create a new URL entry"""
        url_data['created_at'] = datetime.utcnow()
        url_data['updated_at'] = datetime.utcnow()
        
        try:
            result = self.collection.insert_one(url_data)
            url_data['_id'] = result.inserted_id
            return url_data
        except DuplicateKeyError:
            return None
    
    def find_by_id(self, url_id):
        """Find a URL by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(url_id)})
        except:
            return None
    
    def find_all(self, filters=None, search=None, tag=None, page=1, per_page=24):
        """Find URLs with optional filters, search, and pagination"""
        query = {}
        
        # Text search
        if search:
            query['$text'] = {'$search': search}
        
        # Tag filter
        if tag:
            query['tags'] = tag
        
        # Apply additional filters
        if filters:
            query.update(filters)
        
        # Calculate skip
        skip = (page - 1) * per_page
        
        # Get results with pagination
        cursor = self.collection.find(query).sort('created_at', -1).skip(skip).limit(per_page)
        urls = list(cursor)
        
        # Get total count
        total = self.collection.count_documents(query)
        
        return {
            'urls': urls,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def update(self, url_id, url_data):
        """Update a URL entry"""
        url_data['updated_at'] = datetime.utcnow()
        
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(url_id)},
                {'$set': url_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete(self, url_id):
        """Delete a URL entry"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(url_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_all_tags(self):
        """Get all unique tags with counts"""
        pipeline = [
            {'$unwind': '$tags'},
            {'$group': {
                '_id': '$tags',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return [{'tag': item['_id'], 'count': item['count']} for item in result]
    
    def get_stats(self):
        """Get collection statistics"""
        total_urls = self.collection.count_documents({})
        tags = self.get_all_tags()
        total_tags = len(tags)
        
        return {
            'total_urls': total_urls,
            'total_tags': total_tags,
            'tags': tags
        }


# Singleton instance
url_repo = URLRepository()
