from pymongo import MongoClient
import os

db = None

def init_mongo(app):
    global db
    uri = os.getenv('MONGODB_URI')
    if not uri:
        raise ValueError("MONGODB_URI is not set in environment variables")
    
    client = MongoClient(uri)
    # Get database name from URI or default to 'portfolio_db'
    db_name = uri.split('/')[-1].split('?')[0] or 'portfolio_db'
    db = client[db_name]
    
    # Verify connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
