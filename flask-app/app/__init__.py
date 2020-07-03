# from flask import Flask, render_template, current_app
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_assets import Environment
from .assets import create_assets
from .routes import auth_bp, api_bp, main_bp, auth_pages, movies_bp
from flask_login import LoginManager
from .login_manager import manage_login


# auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
from .routes.admin_panel import admin_panel_pb
from .routes.user_profile import user_profile_pb


def create_app(config_name):
    app = Flask(__name__)
    Bootstrap(app)
    app.secret_key = b'\xdf\xc0\xe8\xb0\x14\xb2\xad\x9f\x1c\xc19\x87/4\x19v\x11\xa8%I\xad=\x8f\x86'
    # for testing
    # app.config['WTF_CSRF_ENABLED'] = False

    csrf = CSRFProtect()
    csrf.init_app(app)

    login_mng = LoginManager()
    login_mng.init_app(app)

    manage_login(login_mng)

    assets = Environment(app)
    create_assets(assets)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_pages)
    app.register_blueprint(movies_bp)
    app.register_blueprint(admin_panel_pb)
    app.register_blueprint(user_profile_pb)

    register_error_pages(app)

    return app


def register_error_pages(app):

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('403.html'), 403
