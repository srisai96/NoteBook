import webapp2
import templater
from models import BlogModel, UserModel
from cookies import getUserFromRequest
import logging
import time


class EditBlogHandler(webapp2.RequestHandler):
    def get(self, blog_id):
        user = getUserFromRequest(self.request)  # type: UserModel
        post = BlogModel.get_by_id(int(blog_id))  # type:BlogModel

        if not user:
            # redirect to sign up page in case user is not found in the db
            self.redirect("/signin")
        elif not post:
            self.response.write("blog entry not found")
        elif post.author.key().id() == user.key().id():
            self.response.write(templater.render_edit_post(post=post))
        else:
            # redirect to users blog entries to choose one
            self.redirect('/blog/all')

    def post(self, blog_id):
        title = self.request.get("title")
        content = self.request.get("content")
        post = BlogModel.get_by_id(long(blog_id))  # type:BlogModel
        user = getUserFromRequest(self.request)  # type: UserModel
        if title and content and post.author.key().id() == user.key().id():
            # user is authorised to make changes
            if self.request.get('edit'):
                # update the post contents
                post.content = content
                post.title = title
                post.put()
                self.redirect("/blog/%s" % (blog_id))
            elif self.request.get('delete'):
                # delete post is triggered and got confirmation from user
                post.delete()
            # redirect to user home. If we return user entries, it will list old posts as well
            self.redirect('/welcome')
        elif user:
            # redirect to user blog entries
            self.redirect('/blog/user')
        else:
            self.redirect("/signin")
