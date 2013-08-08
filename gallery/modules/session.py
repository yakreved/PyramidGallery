from gallery.models import User
from gallery import Session


def checkuser(username,userpass):
    session = Session()
    ourUser = session.query(User).filter_by(name=username, password=userpass).first()
    if ourUser is None:
        return False
    print("user connected: " + ourUser.name)
    return ourUser


def nosession(request):
    if 'username' in request.cookies and 'userpass' in request.cookies:
        session = Session()
        user = session.query(User).filter_by(name=request.cookies['username'], password=request.cookies['userpass']).first()
        return user is None
    print("user has no session")
    return True

def getOurUser(request):
    session = Session()
    return session.query(User).filter_by(name=request.cookies['username'],
                                                password=request.cookies['userpass']).first()