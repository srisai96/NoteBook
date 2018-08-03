import hmac
from models import UserModel


def getHashForUserid(userid):
    return hmac.new(str(userid), '5cdaae38582e3f1f9a17f7025').hexdigest()


def getCookieHashForUserid(userid):
    return "%s|%s" % (userid, getHashForUserid(userid))


def checkCookieHash(userid_with_hash):
    (userid, namehash) = userid_with_hash.split("|")
    return namehash == getHashForUserid(userid)


def getUserFromRequest(request):
    """
    get the user name from the cookie; if it is tampered return None; No user found - returns None
    :param request: Request object
    :return: Username or None
    """
    if hasattr(request, 'cookies') and \
            request.cookies and \
                    'user_id' in request.cookies and \
            checkCookieHash(request.cookies['user_id']):
        userid = request.cookies['user_id'].split("|")[0]
        return UserModel.get_by_id(long(userid))  # type: UserModel


if __name__ == '__main__':
    print checkCookieHash('5207287069147136|a629ce30034890db295020e4c2397caf')
