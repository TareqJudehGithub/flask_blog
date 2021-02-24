from flask import Flask, render_template

# Create a flask instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
def index():
    """Main webpage"""
    first_name = "john smith"
    stuff = "This is <strong>bold text</strong>."

    return render_template(
        "index.html",
        first_name=first_name,
        stuff=stuff
    )


# Create a custom route
@app.route("/user")
def user():
    names = ["john", "sarah", "emma", "jennah", "noor", "dina", "leen"]

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
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()
