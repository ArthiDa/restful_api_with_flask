from flask import Flask, url_for, request
from markupsafe import escape


# we create an instance of Flask class. The first argument is the name of the application’s module or package.
app = Flask(__name__)

# We use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def index():
    return "Index Page"


# HTML Escaping
# <name> in the route captures a value from the URL and passes it to the view function.
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


# Variable Rules
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

# Unique URLs / Redirection Behavior
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

# URL Building
@app.route('/login')
def login():
    return 'login'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('show_user_profile', username='Arthi Da'))


# HTTP Methods
# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

if __name__ == '__main__':
    app.run(debug=True)
