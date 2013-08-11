import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

from gallery.models import User, Image, Comment
from gallery.views.v_layout import site_layout
from gallery import Session
from gallery.modules.session import nosession, getOurUser
from gallery.modules.imagefiles import deleteImageFile, addImageFile


@view_config(route_name='addImage', renderer='gallery:templates/add.pt')
def addImage(request):
    if nosession(request):
        return HTTPFound(location="/login")
    ourUser = getOurUser(request)
    if request.method == "POST":
        session = Session()
        print('addind image by ' + ourUser.name)
        f = request.POST['image']
        if not hasattr(f, "filename") or not hasattr(f, "file"):
            return {'layout': site_layout(), 'page_title': 'Add Image', 'ourUser': ourUser}
        addImageFile(f.filename, f.file)
        img = Image(request.params['name'], request.params['description'],
                    '../static/images/' + request.POST['image'].filename,
                    datetime.datetime.now(), fk_owner=ourUser.id)
        session.add(img)
        session.commit()
    return {'layout': site_layout(), 'page_title': 'Add Image', 'ourUser': ourUser}


@view_config(route_name='image', renderer='gallery:templates/image.pt')
def image(request):
    if nosession(request):
        return HTTPFound(location="/login")
    name = request.matchdict['imagename']
    session = Session()
    ourUser = getOurUser(request)
    image = session.query(Image).filter_by(id=name).one()
    user = session.query(User).filter_by(id=image.fk_owner).one()
    comments = session.query(Comment).filter_by(fk_image=image.id).all()
    print("User admin - "+ str(user.isadmin)+ "    "+ str(ourUser))
    return dict(
        layout=site_layout(),
        page_title=image.name,
        image=image,
        user=user,
        comments=comments,
        nodelete=(ourUser.id != user.id and not ourUser.isadmin),
        save_url=request.route_url('image', imagename=name),
        ourUser=ourUser
    )


@view_config(route_name='delImage')
def delImage(request):
    if nosession(request):
        return HTTPFound(location="/login")
    image_id = request.params["image_id"]
    print("Deleting Image" + image_id)
    session = Session()
    image = session.query(Image).filter_by(id=image_id).first()
    deleteImageFile(image)
    session.delete(image)
    session.commit()
    return Response("success")


@view_config(route_name='addComment')
def addComment(request):
    if nosession(request):
        return HTTPFound(location="/login")
        #print("Adding comment")
    image_id = request.params["imageid"]
    session = Session()
    image = session.query(Image).filter_by(id=image_id).first()
    ourUser = getOurUser(request)
    com = Comment(ourUser.id, image.id, datetime.datetime.now(), request.params['message'])
    session.add(com)
    session.commit()
    return HTTPFound('/image/' + image_id)