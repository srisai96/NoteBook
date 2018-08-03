import webapp2
import templater
import logging
from models import BlogModel
from cookies import getUserFromRequest


class BlogsHandler(webapp2.RequestHandler):
    # list all the blog posts - default landing page
    def get(self):
        posts = BlogModel.all()
        posts.order('-modified_time')
        # check whether a user has signed in to the site
        userSignedIn = getUserFromRequest(self.request) is not None  # type: bool
        self.response.write(
            templater.render_all_post(posts=posts, userSignedIn=userSignedIn)
        )


class UserPostsHandler(webapp2.RequestHandler):
    # list all user specific posts
    def get(self):
        posts = BlogModel.all()
        user = getUserFromRequest(self.request)
        posts.filter('author = ', user)
        posts.order('-modified_time')
        length = posts.count()

        if user:
            self.response.write(
                templater.render_all_post(
                    posts=posts, length=length,
                    userSignedIn=True
                )
            )
        else:
            self.redirect('/signin')
