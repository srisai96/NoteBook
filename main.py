#!/usr/bin/env python

import webapp2
from handlers import *
from handlers.friendprofile import FriendProfile
from handlers.friends import AddFriendsHandler


class RedirecterHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog/all")


routes = [
    ('/', RedirecterHandler),
    ('/blog', RedirecterHandler),
    ('/welcome', WelcomeHandler),
    ('/blog/all', BlogsHandler),
    ('/blog/new', CreateBlogHandler),
    ('/blog/(\d+)/edit', EditBlogHandler),
    ('/blog/(\d+)', BlogHandler),
    ('/blog/user', UserPostsHandler),
    ('/signup', SignupHandler),
    ('/signin', SigninHandler),
    ('/signout', SignoutHandler),
    ('/blog/friends', AddFriendsHandler),
    ('/blog/friends/(\d+)', FriendProfile)
]

app = webapp2.WSGIApplication(routes=routes, debug=True)
