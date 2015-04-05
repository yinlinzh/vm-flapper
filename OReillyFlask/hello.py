# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import Flask, request, make_response, abort, redirect, render_template, \
                  url_for, session, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

# Create an application instance, an object of class Flask
# The only required argument to the Flask class constructor
# is the name of the main module or package of the application.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mgr = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


mgr.add_command('shell', Shell(make_context=make_shell_context))
mgr.add_command('db', MigrateCommand)


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.username)


class NewModel(db.Model):
    __tablename__ = 'newmodel'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.id)


# view function
# A response returned by a view function can be a simple string
# with HTML content
# The methods argument added to the app.route decorator tells Flask to register the view function
# as a handler for GET and POST requests in the URL map.
# When methods is not given, the view function is registered to handle GET requests only.
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # The local "name" variable is now placed in the user session as session['name'] so that
        # it is remembered beyond the request.
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           name=session.get('name'),
                           form=form,
                           known=session.get('known', False))
    # user_agent = request.headers.get('User-Agent')
    # response = make_response('<h1>Your User-Agent is %s\n,
    # This document carries a cookie!</h1>' % user_agent)
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
    mgr.run()
    # app.run(debug=True)
