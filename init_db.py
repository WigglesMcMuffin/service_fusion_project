from flask_app import create_app
from flask_app.models.base import db, User

if __name__ == '__main__':
    app = create_app(env='prod')
    with app.app_context():
        db.create_all()
