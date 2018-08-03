import webapp2
import time
import templater
from models import BlogModel, UserModel, CommentModel
from cookies import getUserFromRequest


class FriendProfile(webapp2.RequestHandler):

    def get(self, friend_id):
        length = 0
        friend = UserModel.get_by_id(long(friend_id))
        if friend:
            posts = BlogModel.all()
            posts.filter('author = ', friend)
            posts.order('-modified_time')
            length = posts.count()
            user = getUserFromRequest(self.request)
            if user:
                self.response.write(
                    templater.render_friendprofile(userSignedIn=True, posts=posts, friend_id=friend_id, user=user,
                                                   length=length,
                                                   friend=friend))
            else:
                self.redirect("/")

        else:
            self.response.write("Friend entry not found")
