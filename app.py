from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

# Create a flask instance
app = Flask(__name__)

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY
year = datetime.now().year


# Create a Form class
class NameForm(FlaskForm):
    name = StringField("Enter your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
    """Main webpage"""
    first_name = "john smith"
    stuff = "This is <strong>bold text</strong>."
    flash("Welcome to my blog page!")

    return render_template(
        "index.html",
        first_name=first_name,
        stuff=stuff
    )


# Create a custom route
@app.route("/user")
def user():
    names = ["john", "sarah", "emma", "adam", "noor", "dina", "leen"]

    return render_template("user.html", users=names)


# Creating a grocery list route page:
@app.route("/grocery")
def grocery():
    grocery_list = ["bread", "milk", "cereal", "peanut butter", 41]
    return render_template("grocery.html", grocery=grocery_list)


# Create custom error pages
# 1. Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


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


# Adding year to base.html page
@app.route("/base")
def add_year():
    return render_template("base.html", year=year)


if __name__ == '__main__':
    app.run()
