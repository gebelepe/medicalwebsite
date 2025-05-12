from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'

    from .views import views
    app.register_blueprint(views,url_prefix='/')
    from .formlogic import formlogic
    app.register_blueprint(formlogic,url_prefix='/')

    return app

