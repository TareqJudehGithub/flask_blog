from flask import Flask, render_template, flash

# Flask wtforms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

# Flask SQL Alchemy:
from flask_sqlalchemy import SQLAlchemy


from datetime import datetime
import os


# Create a flask instance
app = Flask(__name__)

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY

year = datetime.now().year
date = datetime.now().date()

# SQL alchemy initialization:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app=app)


# Create a db model:
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=date)

    def __repr__(self):
        return f"User: {self.id}, {self.user}, {self.email}"


# Create the db: Just run this once.
# db.create_all()

class UsersForm(FlaskForm):
    user = StringField("Name", validators=[DataRequired()])
    email = EmailField("example@email.com", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


# Create a Form class
class NameForm(FlaskForm):
    name = StringField("Enter your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
    """Main webpage"""
    flash("Welcome to my blog page!")

    return render_template(
        "index.html"
    )


# Create a custom route
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    form = UsersForm()
    user = None
    email = None
    users_list = Users.query.order_by(Users.user)

    if form.validate_on_submit():
        try:
            # Add submit data to the database:
            user = Users(user=form.user.data, email=form.email.data)

            # Save data in the database:
            db.session.add(user)
            db.session.commit()

            user = form.user.data
            form.user.data = ""
            email = form.email.data
            form.email.data = ""
            message = flash("User added successfully!")


        except:
            return "Error saving user in the database."
        else:
            return render_template(
                "user.html",
                form=form,
                user=user,
                email=email,
                message=message,
                users_list=users_list,
                year=year
            )

    return render_template(
        "user.html",
        form=form,
        user=user,
        email=email,
        users_list=users_list,
        year=year
    )


# Create Name page:
@app.route("/name", methods=["GET", "POST"])
def name():
    user_name = None         # name variable from NameForm class
    form = NameForm()   # NameForm() class
    # Validation Form
    # When users submit a form:
    if form.validate_on_submit():
        # Assign name entered to user_name:
        user_name = form.name.data
        # Clear the form after:
        form.name.data = ""

        # Flash messages:
        flash("Form submitted successfully!")

    return render_template(
        "name.html",
        name=user_name,
        form=form
    )


# Create custom error pages
# 1. Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


# Adding year to base.html page
@app.route("/base")
def add_year():
    return render_template("base.html", year=year)


if __name__ == '__main__':
    app.run()
