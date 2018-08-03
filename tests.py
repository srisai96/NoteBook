import unittest
import os
from google.appengine.api import apiproxy_stub_map, datastore_file_stub
from models import *
from google.appengine.ext import db


class SomeTestCase(unittest.TestCase):
    def setUp(self):
        app_id = 'myapp'
        os.environ['APPLICATION_ID'] = app_id
        datastore_file = '/dev/null'
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        stub = datastore_file_stub.DatastoreFileStub(app_id, datastore_file, '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    def testUserDb(self):
        self.setUp()
        UserModel.createNewUser(name="user1", pwd="pwd1").put()
        UserModel.createNewUser(name="user2", pwd="pwd2").put()
        UserModel.createNewUser(name="user3", pwd="pwd3").put()
        assert db.Query(UserModel).filter('name = ', "user1").get().name == "user1"
        assert db.Query(UserModel).filter('name = ', "user5").get() == None
        assert db.Query(UserModel).filter('name = ', 'user1').get().checkPassword('pwd1') == True
        assert db.Query(UserModel).filter('name = ', 'user1').get().checkPassword('pwd2') == False
        print "hashed salted password ", db.Query(UserModel).filter('name = ', "user2").get().pwd


if __name__ == '__main__':
    unittest.main()
