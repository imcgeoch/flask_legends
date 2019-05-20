from flask import Blueprint

bp = Blueprint('explorer', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return "Hello, world!"
