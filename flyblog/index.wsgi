import sae
from flyblog import wsgi

application=sae.create_wsgi_app(wsgi.application)
