from flask import Flask
import pyjade
from flask_wtf.csrf import CsrfProtect
from flask_app.models import db, ma
from flask_app.middleware.reverse_proxy import ReverseProxied

csrf = CsrfProtect()

def create_app(debug=False, testing=False):
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'service_fusion_secret_key'
  app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
  app.wsgi_app = ReverseProxied(app.wsgi_app)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@db/service_fusion'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  ma.init_app(app)
  csrf.init_app(app)

  from flask_app.views.main import main_site
  from flask_app.views.users import user_site
  app.register_blueprint(main_site)
  app.register_blueprint(user_site)

  return app
