# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)

# It is important to note that the modules are imported at the bottom of the app/__init__.py script
# to avoid circular dependencies, because views.py and errors.py need to import the main blueprint.
from . import views, errors
