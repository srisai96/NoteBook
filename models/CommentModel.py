from google.appengine.ext import db
from datetime import datetime
from .UserModel import UserModel
from .BlogModel import BlogModel


class CommentModel(db.Model):
    content = db.TextProperty(required=True)  # type: str
    # blog post that the comment belongs to
    post = db.ReferenceProperty(BlogModel, collection_name='comments', required=True)  # type: BlogModel
    # commenter
    author = db.ReferenceProperty(UserModel, collection_name='comments', required=True)  # type:UserModel
    created_time = db.DateTimeProperty(auto_now_add=True)  # type:datetime
    modified_time = db.DateTimeProperty(auto_now=True)  # type:datetime

    def get_content(self):
        return self.content.replace("\n", "<br/>")

    def get_author_name(self):
        return "Anonymous" if not self.author else self.author.name

    def get_modified_time(self):
        return self.modified_time.strftime("%b %d, %y at %I:%M %p")
