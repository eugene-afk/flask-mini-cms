from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(500))
    @property
    def shorter_name(self):
        return text_shorter(self.name, 80)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    title = db.Column(db.String(250))
    title_translation_id = db.Column(db.String(250))
    shortDesc = db.Column(db.String(250))
    shortDesc_translation_id = db.Column(db.String(250))
    full = db.Column(db.String)
    full_translation_id = db.Column(db.String)
    imgMain = db.Column(db.String(250))
    published = db.Column(db.Boolean)
    publishDate = db.Column(db.DateTime)
    lastUpdated = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer)

    @property
    def shorter_name(self):
        return text_shorter(self.title, 100)

    def serialize_short(self, lang):
        tags = Tag.query.join(PostTag, Tag.id == PostTag.tag_id).filter_by(post_id=self.id).all()
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title if not lang else Translation.query.filter_by(lang=lang, translation_id=self.title_translation_id).first().text,
            'shortDesc': self.shortDesc if not lang else Translation.query.filter_by(lang=lang, translation_id=self.shortDesc_translation_id).first().text,
            'img': self.imgMain,
            'publishDate': self.publishDate.strftime("%Y-%m-%d %H:%M"),
            'author': User.query.filter_by(id=self.owner_id).first().name,
            'tags': [e.serialize() for e in tags]

        }

    def serialize(self, lang):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title if not lang else Translation.query.filter_by(lang=lang, translation_id=self.title_translation_id).first().text,
            'shortDesc': self.shortDesc if not lang else Translation.query.filter_by(lang=lang, translation_id=self.shortDesc_translation_id).first().text,
            'img': self.imgMain,
            'lastUpdated': self.lastUpdated.strftime("%Y-%m-%d %H:%M"),
            'full': self.full if not lang else Translation.query.filter_by(lang=lang, translation_id=self.full_translation_id).first().text,
            'publishDate': self.publishDate.strftime("%Y-%m-%d %H:%M"),
            'author': User.query.filter_by(id=self.owner_id).first().name
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(250), unique=True)
    translation_id = db.Column(db.String(250))
    @property
    def shorter_name(self):
        return text_shorter(self.category_name, 80)
    def serialize(self, lang):
        return {
            'category_id': self.id,
            'category_name': self.category_name if not lang else Translation.query.filter_by(lang=lang, translation_id=self.translation_id).first().text 
        }

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(250), unique=True)
    @property
    def shorter_name(self):
        return text_shorter(self.tag_name, 80)
    def serialize(self):
        return {
            'tag_name': self.tag_name
        }

class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_extension = db.Column(db.String)
    pure_name = db.Column(db.String)
    media_name = db.Column(db.String)
    def serialize(self):
        return{
            'media_name': self.media_name,
            'original_extension': self.original_extension,
            'pure_name': self.pure_name
        }

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    translation_id = db.Column(db.String)
    lang = db.Column(db.String)
    text = db.Column(db.String)
    def serialize(self):
        return{
            'text': self.text
        }

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String)
    lang_name = db.Column(db.String)

    def serialize(self):
        return{
            "lang_name": self.lang_name,
            "lang_code": self.lang_code,
        }

def text_shorter(txt, length):
    if len(txt) > length:
        txt = txt[:-(len(txt) - length)] + '...'
    return txt
