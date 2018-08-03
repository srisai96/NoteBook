from google.appengine.ext import db
from datetime import datetime
from .UserModel import UserModel
import logging

class BlogModel(db.Model):
    title = db.StringProperty(required=True)  # type: str
    content = db.TextProperty(required=True)  # type: str
    # username of writer
    author = db.ReferenceProperty(UserModel, collection_name='posts')  # type:UserModel
    # to count the likes for the post and store the user_id in the list
    likes = db.ListProperty(item_type=long, write_empty_list=True)  # type: list
    likescount = db.IntegerProperty(default=0)
    created_time = db.DateTimeProperty(auto_now_add=True)  # type:datetime
    modified_time = db.DateTimeProperty(auto_now=True)  # type:datetime

    def get_content(self, truncate=False):
        if truncate:
            return ("\n".join(self.content.split('\n')[:10])).replace('\n', "<br/>")
        return self.content.replace("\n", "<br/>")

    def get_created_time(self):
        return self.created_time.strftime("%b %d, %y at %I:%M %p")

    def get_perma_link(self):
        return "/blog/%s" % (self.key().id())

    def get_author_name(self):
        return "Anonymous" if not self.author else self.author.name

    def get_modified_time(self):
        return self.modified_time.strftime("%b %d, %y at %I:%M %p")

    def get_comments_ordered(self):
        # return comments ordered based on their created time
        return self.comments.order('created_time')

    def get_likes_count(self):
        """
        :return: number of likes for the post
        """
        return len(self.likes)
