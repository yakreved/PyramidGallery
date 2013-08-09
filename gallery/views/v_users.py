from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from gallery.models import User
from gallery import Session
from gallery.views.v_layout import site_layout
from pyramid.response import Response
from gallery.modules.session import nosession,getOurUser


@view_config(route_name='users', renderer='gallery:templates/users.pt')
def users(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    session = Session()
    users = session.query(User).all()
    return {'layout':site_layout(),'page_title':'Users of gallery', 'users':users, 'ourUser': getOurUser(request)}


@view_config(route_name='deleteUser')
def deleteUser(request):
    print("Deleting user")
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
