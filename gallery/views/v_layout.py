from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.response import Response

from gallery.models import Image
from gallery import Session
from gallery.modules.session import nosession, getOurUser


def site_layout():
    renderer = get_renderer("gallery:templates/base.pt")
    layout = renderer.implementation().macros['layout']
    return layout


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
    return {'layout':site_layout(), 'page_title': 'Users of gallery', 'images': images, "ourUser": getOurUser(request)}
