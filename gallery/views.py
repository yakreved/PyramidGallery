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
    renderer = get_renderer("templates/base.pt")
    layout = renderer.implementation().macros['layout']
    return layout

@view_config(route_name='login', renderer='templates/login.pt')
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


@view_config(route_name='users', renderer='templates/users.pt')
def users(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    session = Session()
    users = session.query(User).all()
    return {'layout':site_layout(),'page_title':'Main page of gallery', 'users':users}


@view_config(route_name='home', renderer='templates/main.pt')
def my_view(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    session = Session()
    images = session.query(Image).order_by(Image.date.desc()).all()[:5]
    return {'layout':site_layout(),'page_title':'Users of gallery', 'images':images}


@view_config(route_name='addImage', renderer='templates/add.pt')
def addImage(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    if request.method=="POST":
        session = Session()
        ourUser = session.query(User).filter_by(name=request.cookies['username'], password=request.cookies['userpass']).first()
        print('addind image by '+ ourUser.name)
        _here = os.path.dirname(__file__)
        input_file = request.POST['image'].file
        tmp = os.path.join(_here,'static','images', request.POST['image'].filename) 
        open(tmp, 'wb').write(input_file.read())
        img = Image(request.params['name'], request.params['description'], '../static/images/'+request.POST['image'].filename, datetime.datetime.now(),fk_owner=ourUser.id)
        session.add(img)
        session.commit()
    return {'layout':site_layout(),'page_title':'Add Image'}


@view_config(route_name='deleteUser')
def deleteUser(request):
    print("Deleting user")
    print(request.params)
    session = Session()
    our_user = session.query(User).filter_by(id=request.params['id']).first()
    print(our_user.name + 'deleted')
    session.delete(our_user)
    session.commit()
    return Response("success")


@view_config(route_name='addUser')
def addUser(request):
    session = Session()
    newuser = User(request.params["username"],
        request.params["userpass"])
    session.add(newuser)
    session.commit()
    return HTTPFound("/users")

@view_config(route_name='image', renderer='templates/image.pt')
def image(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    name = request.matchdict['imagename']
    session = Session()
    image = session.query(Image).filter_by(id = name).one()
    user = session.query(User).filter_by(id = image.fk_owner).one()
    return dict(
        layout=site_layout(),
        page_title=image.name,
        image=image,
        user=user,
        save_url = request.route_url('image', imagename=name),
        )