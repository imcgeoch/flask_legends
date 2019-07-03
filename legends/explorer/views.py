from flask import Blueprint, render_template

from ..models import *
from . import bp

# bp = Blueprint('explorer', __name__, template_folder='templates')

@bp.route('/')
@bp.route('/index')
def index():
    return "Hello, world!"

@bp.route('/worlds')
def world_index():
    worlds = DF_World.query.all()
    return str(worlds)

@bp.route('/<world_id>/histfigs')
def hf_index(world_id):
    hfs = Historical_Figure.query.filter_by(df_world_id=world_id).limit(1000).all()
    print(hfs[781].deity)
    return render_template('histfigs.html', hfs=hfs)
