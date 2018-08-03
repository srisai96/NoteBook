import webapp2
import templater
from models import UserModel
from cookies import getCookieHashForUserid
import logging


class SignoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.delete_cookie('user_id')
        self.redirect('/signin')


class SigninHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(templater.render_signin_page(
            errormsg=self.request.get('errormsg')))

    def post(self):
        username = self.request.get("userName")
        pwd = self.request.get("pwd")
        rememberMe = self.request.get("rememberMe")

        if username and pwd:
            user = getUserByName(username)  # type: UserModel
            if user and user.checkPassword(pwd):
                if rememberMe:
                    import datetime
                    self.response.set_cookie('user_id', str(getCookieHashForUserid(user.key().id())),
                                             expires=(datetime.datetime.now() + datetime.timedelta(days=7)))
                else:
                    self.response.set_cookie('user_id', str(getCookieHashForUserid(user.key().id())))
                self.redirect("/welcome")
            else:
                self.redirect('/signin?errormsg=invalid login')
        else:
            self.redirect('/signin?errormsg=invalid login')


class SignupHandler(webapp2.RequestHandler):
    def get(self):
        errormsg = self.request.get("errormsg")
        self.response.write(templater.render_signup_page(errormsg=errormsg))

    def post(self):
        username = self.request.get("userName")
        pwd = self.request.get("pwd")
        email = self.request.get("email")
        if username and pwd:
            if getUserByName(username):
                # username already exists
                self.redirect('/signup?errormsg=username_exists')
                return
            # add user to db
            user = UserModel.createNewUser(username, pwd, email)
            user.put()
            self.response.set_cookie('user_id', str(getCookieHashForUserid(user.key().id())))
            self.redirect("/welcome")
        else:
            self.redirect("/signup?errormsg=invalid_data")


def getUserByName(username):
    # check and return user db object
    return UserModel.all().filter("name = ", username).get()
