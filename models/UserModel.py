from google.appengine.ext import db
import templater
from datetime import datetime
import hmac


class UserModel(db.Model):
    name = db.StringProperty(required=True)
    pwd = db.StringProperty(required=True)
    salt = db.StringProperty()
    email = db.EmailProperty()
    friends = db.ListProperty(item_type=long, write_empty_list=True)
    created_time = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        return templater.render_welcome_page(user=self)

    def checkPassword(self, pwd):
        """
        :param pwd: password as plain text
        :type pwd: str
        :return: true if the password is valid
        :rtype: bool
        """
        return hmac.new(str(self.salt), pwd).hexdigest() == self.pwd

    @classmethod
    def createNewUser(cls, name, pwd, email=None):
        """
        :param name: name of the user
        :type name: str
        :param pwd: plain text password
        :type pwd: str
        :param email: optional email param
        :type email: str
        :return: user instance
        :rtype: UserModel
        """
        # automatically create salt and hash passowrd then create an user instance and return
        salt = datetime.now().strftime("%d%m%y%H%M%S")
        pwd = hmac.new(salt, pwd).hexdigest()
        return UserModel(name=name, pwd=pwd, email=email, salt=salt)

    def get_friends_count(self):
        return len(self.friends)