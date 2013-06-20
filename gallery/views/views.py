from pyramid.view import view_config
import os
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from gallery.models import User
from gallery.models import Image
from gallery import Session
from pyramid.renderers import get_renderer
from pyramid.response import Response
import datetime


def checkuser(username,userpass):
    session = Session()
    ourUser = session.query(User).filter_by(name=username, password=userpass).first()
    if ourUser is None:
        return False
    print("user connected: " + ourUser.name)
    return ourUser


def nosession(request):
    if('username' in request.cookies and 'userpass' in request.cookies):
        session = Session()
        user = session.query(User).filter_by(name=request.cookies['username'], password=request.cookies['userpass']).first()
        return user == None 
    print("user has no session")
    return True


def site_layout():
    renderer = get_renderer("gallery:templates/base.pt")
    layout = renderer.implementation().macros['layout']
    return layout

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


@view_config(route_name="logout")
def logout(request):
    response = Response()
    response.set_cookie('username', value=None)
    return HTTPFound(location = "/login", headers=response.headers)


@view_config(route_name='home', renderer='gallery:templates/main.pt')
def my_view(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    session = Session()
    images = session.query(Image).order_by(Image.date.desc()).all()[:5]
    return {'layout':site_layout(),'page_title':'Users of gallery', 'images':images}
