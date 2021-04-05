from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
#from flask_uploads import IMAGES,UploadSet, configure_uploads, patch_request_class
from werkzeug.utils import secure_filename
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'v\xf9\xf7\x11\x13\x18\xfaMYp\xed_\xe8\xc9w\x06\x8e\xf0f\xd2\xba\xfd\x8c\xda'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lab5:123@localhost/lab5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir, 'static/uploads')

#photos = UploadSet('photos', IMAGES)
#configure_uploads(app,photos)
#patch_request_class(app)


db = SQLAlchemy(app)
bcrypt=  Bcrypt(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(Config)
from app import views
from app.products import views
from app.carts import carts