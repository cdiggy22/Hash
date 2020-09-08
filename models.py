from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.Text(), primary_key = True, unique=True)
    password = db.Column(db.Text(), nullable = False)
    email = db.Column(db.Text(), nullable= False, unique=True)
    first_name = db.Column(db.Text(), nullable = False)
    last_name = db.Column(db.Text(), nullable = False)

    @classmethod 
    def register(cls, username, password, email, first_name, last_name):
        """ register user and hash password"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """authenticate email and password being logged in"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer(), primary_key = True, unique=True, autoincrement=True)
    title = db.Column(db.Text(), nullable = False)
    content = db.Column(db.Text(), nullable= False)
    username = db.Column(db.Text(), db.ForeignKey('users.username'), nullable = False)
    


   