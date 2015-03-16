# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask, request, make_response, abort, redirect, render_template, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

# Create an application instance, an object of class Flask
# The only required argument to the Flask class constructor
# is the name of the main module or package of the application.
app = Flask(__name__)
mgr = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


# view function
# A response returned by a view function can be a simple string
# with HTML content
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
    # user_agent = request.headers.get('User-Agent')
    # response = make_response('<h1>Your User-Agent is %s\n, This document carries a cookie!</h1>' % user_agent)
    # response.set_cookie('answer', '42')
    # return response
    # return '<p>Your browser is %s</p>' % user_agent
    # return 'Bad xxx request', 400
    # return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    url = url_for('user', name=name, _external=True)
    return render_template('user.html', name=name, url=url)
    # abort(404)
    # return '<h1>Hello, %s!</h1>' % name


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # mgr.run()
    app.run(debug=True)
