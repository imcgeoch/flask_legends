from flask import Blueprint

#bp = Blueprint('explorer', __name__)
bp = Blueprint('explorer', __name__, template_folder='templates')

from . import views
