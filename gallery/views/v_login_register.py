from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from gallery.modules.session import checkuser
from gallery.models import User
from gallery import Session


def set_session_cookies(response, username, userpass):
    response.set_cookie('username', value=username, max_age=86400)
    response.set_cookie('userpass', value=userpass, max_age=86400)
    print("cookies setted for user "+ username)


@view_config(route_name='login', renderer='gallery:templates/login.pt')
def login(request):
    if request.method == "POST":
        username = request.params['username']
        userpass = request.params['userpass']
        if checkuser(username, userpass):
            response = Response()
            set_session_cookies(response, username, userpass)
            return HTTPFound(location="/", headers=response.headers)
        return {'message': 'Wrong login or password'}
    return {'message': "Welcome!"}

@view_config(route_name='register')
def register(request):
    session = Session()
    newuser = User(request.params["username"],
        request.params["userpass"], False)
    session.add(newuser)
    session.commit()
    response = Response()
    set_session_cookies(response, request.params["username"],
                        request.params["userpass"])
    return HTTPFound(location = "/", headers=response.headers)