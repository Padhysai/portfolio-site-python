from datetime import datetime
from . import mongo

import re
import html

def _unescape_case_study(case_study):
    if not case_study:
        return None
    for field in ['challenge', 'solution', 'impact', 'content']:
        if field in case_study and case_study[field]:
            case_study[field] = html.unescape(case_study[field])
    return case_study

def get_all_case_studies():
    if mongo.db is not None:
        cursor = mongo.db.case_studies.find().sort('date', -1)
        return [_unescape_case_study(cs) for cs in cursor]
    return []

def save_case_study(title, tags, challenge, solution, impact, content):
    if mongo.db is not None:
        slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))
        tag_list = [t.strip() for t in tags.split(',')] if tags else []
        
        case_study = {
            'id': slug,
            'title': title,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': tag_list,
            'challenge': challenge,
            'solution': solution,
            'impact': impact,
            'content': content
        }
        
        mongo.db.case_studies.update_one(
            {'id': slug},
            {'$set': case_study},
            upsert=True
        )
        return True
    return False

def update_case_study(id, title, tags, challenge, solution, impact, content):
    if mongo.db is not None:
        tag_list = [t.strip() for t in tags.split(',')] if tags else []
        
        case_study = {
            'title': title,
            'tags': tag_list,
            'challenge': challenge,
            'solution': solution,
            'impact': impact,
            'content': content
        }
        
        mongo.db.case_studies.update_one(
            {'id': id},
            {'$set': case_study}
        )
        return True
    return False

def get_case_study_by_id(id):
    if mongo.db is not None:
        cs = mongo.db.case_studies.find_one({'id': id})
        return _unescape_case_study(cs)
    return None

def delete_case_study(id):
    if mongo.db is not None:
        mongo.db.case_studies.delete_one({'id': id})
        return True
    return False
