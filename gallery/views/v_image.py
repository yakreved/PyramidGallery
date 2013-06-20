from pyramid.view import view_config
import os
import threading
import time
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from gallery.models import User
from gallery.models import Image
from gallery.views.views import nosession,site_layout
from gallery import Session
from pyramid.renderers import get_renderer
from pyramid.response import Response
import datetime


@view_config(route_name='addImage', renderer='gallery:templates/add.pt')
def addImage(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    if request.method=="POST":
        session = Session()
        ourUser = session.query(User).filter_by(name=request.cookies['username'], 
                                                password=request.cookies['userpass']).first()
        print('addind image by '+ ourUser.name)
        _here = os.path.split(os.path.dirname(__file__))[0]
        input_file = request.POST['image'].file
        tmp = os.path.join(_here,'static','images', request.POST['image'].filename) 
        open(tmp, 'wb').write(input_file.read())
        img = Image(request.params['name'], request.params['description'],
                     '../static/images/'+request.POST['image'].filename,
                      datetime.datetime.now(),fk_owner=ourUser.id)
        session.add(img)
        session.commit()
    return {'layout':site_layout(),'page_title':'Add Image'}


@view_config(route_name='image', renderer='gallery:templates/image.pt')
def image(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    name = request.matchdict['imagename']
    session = Session()
    ourUser = session.query(User).filter_by(name=request.cookies['username'], password=request.cookies['userpass']).first()
    image = session.query(Image).filter_by(id = name).one()
    user = session.query(User).filter_by(id = image.fk_owner).one()
    nodelete=True
    if(ourUser==user):
        nodelete=False
    return dict(
        layout=site_layout(),
        page_title=image.name,
        image=image,
        user=user,
        nodelete=nodelete,
        save_url = request.route_url('image', imagename=name),
        )


@view_config(route_name='delImage')
def delImage(request):
    if nosession(request):
        return HTTPFound(location = "/login")
    image_id = request.params["image_id"] 
    print("Deleting Image")
    print(image_id)
    session = Session()
    image = session.query(Image).filter_by(id=image_id).first()
    _here = os.path.split(os.path.dirname(__file__))[0]
    tmp = os.path.join(_here,'static','images', os.path.split(image.url)[1])
    session.delete(image)
    session.commit()
    t = threading.Thread(target=deletefile, args=(tmp,))
    t.daemon = True
    t.start()
    return Response("success")


def deletefile(filename):
    print("waiting for delete 5s")
    time.sleep(5)
    print("delete "+ filename)
    os.remove(filename)
    return