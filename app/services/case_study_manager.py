from datetime import datetime
from . import mongo

def get_all_case_studies():
    if mongo.db is not None:
        cursor = mongo.db.case_studies.find().sort('date', -1)
        return list(cursor)
    return []

def save_case_study(title, tags, challenge, solution, impact, content):
    if mongo.db is not None:
        slug = title.lower().replace(' ', '-').replace(r'[^a-z0-9-]', '')
        tag_list = [t.strip() for t in tags.split(',')] if tags else []
        
        case_study = {
            'id': slug,
            'title': title,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': tag_list,
            'challenge': challenge,
            'solution': solution,
            'impact': impact,
            'content': content # Storing HTML/Markdown directly
        }
        
        mongo.db.case_studies.update_one(
            {'id': slug},
            {'$set': case_study},
            upsert=True
        )
        return True
    return False
