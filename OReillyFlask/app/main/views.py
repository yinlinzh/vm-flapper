# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
        # return redirect(url_for('.index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           name=session.get('name'),
                           form=form,
                           known=session.get('known', False))


@main.route('/user/<name>')
def user(name):
    url = url_for('.user', name=name, _external=True)
    return render_template('user.html', name=name, url=url)
