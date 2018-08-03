import webapp2
import time
import templater
from models import BlogModel, UserModel, CommentModel
from cookies import getUserFromRequest


class AddFriendsHandler(webapp2.RequestHandler):

    def get(self):
        user = getUserFromRequest(self.request)
        userfriendsList = []
        if user:
            allusers = UserModel.all()
            currentuser = UserModel.get_by_id(user.key().id())
            userfriendsList = currentuser.friends
            self.response.write(templater.render_friends(userSignedIn=True, allusers=allusers, user=user,
                                                         currentuser = currentuser))
        else:
            self.redirect('/signup')

    def post(self):
        user = getUserFromRequest(self.request)
        userfriendsList = []
        allusers = UserModel.all()
        currentuser = UserModel.get_by_id(user.key().id())
        userfriendsList=currentuser.friends
        addBtnAction = self.request.get('addfriend')

        if addBtnAction:
            otherPersonKey = self.request.get('addfriend')
            if otherPersonKey not in userfriendsList:
                currentuser.friends.append(long(otherPersonKey))
                currentuser.sample = "really!!!"
                currentuser.put()
                time.sleep(0.1)
            self.response.write(templater.render_friends(userSignedIn=True, allusers=allusers, user=user,
                                                         currentuser=currentuser))