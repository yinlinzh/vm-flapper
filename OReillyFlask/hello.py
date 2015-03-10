from flask import Flask, request

# Create an application instance, an object of class Flask
# The only required argument to the Flask class constructor
# is the name of the main module or package of the application.
app = Flask(__name__)


# view function
# A response returned by a view function can be a simple string
# with HTML content
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
    # return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
