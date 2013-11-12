

from wx import db

class DreamObject(db.Document):
    dream_name = db.StringField(max_length=255, required=True)
    dream_content = db.StringFiled(required=True)

    meta = {
        'indexes': ['dream_name']
    }


