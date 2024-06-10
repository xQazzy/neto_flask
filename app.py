from flask import Flask
from models import db
import routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)