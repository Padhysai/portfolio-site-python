from datetime import datetime
from . import mongo

def init_db():
    # MongoDB is initialized in app/__init__.py via mongo.init_mongo
    pass

def increment_view(path):
    if mongo.db is not None:
        mongo.db.page_views.update_one(
            {'path': path},
            {'$inc': {'count': 1}},
            upsert=True
        )

def track_visitor(ip_address):
    if mongo.db is not None:
        first_visit = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Only insert if not exists
        mongo.db.visitors.update_one(
            {'ip_address': ip_address},
            {'$setOnInsert': {'first_visit': first_visit}},
            upsert=True
        )

def get_total_views():
    if mongo.db is not None:
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$count'}}}
        ]
        result = list(mongo.db.page_views.aggregate(pipeline))
        return result[0]['total'] if result else 0
    return 0

def get_unique_visitors():
    if mongo.db is not None:
        return mongo.db.visitors.count_documents({})
    return 0

def get_top_pages(limit=5):
    if mongo.db is not None:
        cursor = mongo.db.page_views.find().sort('count', -1).limit(limit)
        return [(doc['path'], doc['count']) for doc in cursor]
    return []
