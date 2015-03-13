# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, abort, redirect, render_template
from flask.ext.script import Manager

# Create an application instance, an object of class Flask
# The only required argument to the Flask class constructor
# is the name of the main module or package of the application.
app = Flask(__name__)
mgr = Manager(app)


# view function
# A response returned by a view function can be a simple string
# with HTML content
@app.route('/')
def index():
    return render_template('index.html')
    # user_agent = request.headers.get('User-Agent')
    # response = make_response('<h1>Your User-Agent is %s\n, This document carries a cookie!</h1>' % user_agent)
    # response.set_cookie('answer', '42')
    # return response
    # return '<p>Your browser is %s</p>' % user_agent
    # return 'Bad xxx request', 400
    # return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name='<h1>One more time</h1>') #name)
    # abort(404)
    # return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    # mgr.run()
    app.run(debug=True)
