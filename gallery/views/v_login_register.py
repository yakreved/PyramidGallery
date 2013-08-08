from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from gallery.modules.session import checkuser
from gallery.models import User
from gallery import Session


@view_config(route_name='login', renderer='gallery:templates/login.pt')
def login(request):
    if request.method == "POST":
        username = request.params['username']
        userpass = request.params['userpass']
        if checkuser(username, userpass):
            response = Response()
            response.set_cookie('username', value=username, max_age=86400)
            response.set_cookie('userpass', value=userpass, max_age=86400)
            print("cookies setted for user")
            return HTTPFound(location = "/", headers=response.headers)
        return {'message':'Wrong login or password'}
    return {'message':"Welcome!"}

@view_config(route_name='register')
def register(request):
    session = Session()
    newuser = User(request.params["username"],
        request.params["userpass"])
    session.add(newuser)
    session.commit()
    return HTTPFound("/login")