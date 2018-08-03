import webapp2
from google.appengine.ext import db
import templater
from models import *
from cookies import getUserFromRequest
import logging


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        friendscount = 0
        friendnames = []
        friendids = []
        logging.info("checking cookie %s" % self.request.cookies)
        user = getUserFromRequest(self.request)
        currentuser = UserModel.get_by_id(user.key().id())
        for friendid in currentuser.friends:
            temp = UserModel.get_by_id(friendid)
            friendnames.append(temp.name)
            friendids.append(temp.key().id())
        friendscount = len(friendids)
        allposts = db.GqlQuery("select * from BlogModel order by likescount Desc LIMIT 3")
        if user:
            self.response.write(
                templater.render_welcome_page(user=user, friendnames=friendnames, friendids=friendids,
                                              friendscount=friendscount,
                                              userSignedIn=True, allposts=allposts)
            )
        else:
            # redirect to sign up page in case user is not found in the db
            self.redirect("/signup")
