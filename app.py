from flask import Flask, request, render_template, redirect, flash, session, g
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from forms import RegistrationForm, LoginForm, FeedbackForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="postgres:///hash_login"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhhhh2323'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    """Show registration page"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def registration():
    """Handle registration form"""
    
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form=RegistrationForm()

    if form.validate_on_submit():
        try: 
            user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name = form.first_name.data,
            last_name=form.last_name.data
            )

            db.session.add(user)
            db.session.commit()

            session["username"]=user.username

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)


        return redirect (f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad username/password"]

    return render_template('users/login.html', form=form)

@app.route("/users/<username>")
def secret(username):
    """ hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    
    user=User.query.get(username)

    return render_template("users/detail.html", user=user)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/login")

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user."""


    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()

    session.pop("username")

    return redirect("/login")



@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
