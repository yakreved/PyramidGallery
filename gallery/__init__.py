from sqlalchemy import create_engine
from pyramid.config import Configurator
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('users', '/users')
    config.add_route('logout', '/logout')
    config.add_route('deleteUser', '/deleteUser')
    config.add_route('addUser', '/addUser')
    config.add_route('addImage', '/addImage')
    config.add_route('delImage', '/delImage')
    config.add_route('image', '/image/{imagename}')
    config.add_route('addComment', '/addComment')
    config.add_route('home', '/')
    #config.scan()
    config.scan("gallery.views")
    return config.make_wsgi_app()
