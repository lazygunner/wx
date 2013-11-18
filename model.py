
import datetime
from wx import db

class User(db.Document):
    open_id = db.StringField(max_length=255,required=True)
    user_name = db.StringField(max_length=255)
    current_game = db.StringField(max_length=255)
    point = db.IntFiled(default=0)
    created-at = db.DateiTimeField(default=datetime.datetime.now, required=True)

class DreamObject(db.Document):
    dream_name = db.StringField(max_length=255, required=True)
    dream_content = db.StringField(required=True)

    meta = {
        'indexes': ['dream_name']
    }


