import webapp2
import templater
from models import BlogModel
from cookies import getUserFromRequest


class CreateBlogHandler(webapp2.RequestHandler):
    def get(self, errormsg=None):
        user = getUserFromRequest(self.request)
        if user:
            self.response.write(templater.render_new_post(userSignedIn=True))
        else:
            # redirect to sign up page in case user is not found in the db
            self.redirect("/signup")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if title and content:
            post = BlogModel(title=title, content=content)
            user = getUserFromRequest(self.request)
            if user:
                post.author = user
                post.put()
                key = int(post.key().id())
                self.redirect("/blog/%d" % key)
            else:
                self.redirect('/signup')
        else:
            self.redirect("/blog/new")
