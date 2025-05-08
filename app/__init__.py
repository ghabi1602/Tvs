from flask import Flask, session
from .db_storage import db, migrate, init_db
from flask_login import LoginManager
from flask_cors import CORS


login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder='./web_flask/static', template_folder='./web_flask/templates')
    CORS(app)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://tvs_admin:betty@localhost/tvs_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_db(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from .web_flask import authentication
        from .web_flask import routes
        from .api.v1 import api
        from .web_flask import chat
        app.register_blueprint(authentication.bp)
        app.register_blueprint(routes.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(chat.bp)

    @login_manager.user_loader
    def load_user(user_id):
        if session['user_type'] == 'std':
            from .models.student_model import STUDENT
            return STUDENT.query.get(user_id)
        elif session['user_type'] == 'prof':
            from .models.prof_model import PROFESSOR
            return PROFESSOR.query.get(user_id)

    return app

