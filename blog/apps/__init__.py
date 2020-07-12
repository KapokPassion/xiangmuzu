from flask import Flask
from apps.views.blog_view import blog_bp
from exts import db
from settings import DevelopmentConfig

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(DevelopmentConfig)
    app.config["SECRET_KEY"]= 'hello motherfuck'
    #初始化app
    db.init_app(app)

    app.register_blueprint(blog_bp)
    return app