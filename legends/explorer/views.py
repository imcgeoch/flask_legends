from flask import Blueprint, render_template, request

from sqlalchemy import or_

from ..models import *
from . import bp

# bp = Blueprint('explorer', __name__, template_folder='templates')

@bp.app_template_filter('render_event')
def render_event(event):
    return render_template('events/default.html', event=event) 

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
    after = request.args.get('after') or 0
    hfs = Historical_Figure.query\
                           .filter_by(df_world_id=world_id)\
                           .limit(250).offset(after)

    return render_template('histfig_list.html', items=hfs)

@bp.route('/<world_id>/histfig/<hfid>')
def hf_detail(world_id, hfid):
    evt_after = request.args.get('evt_after') or 0
    hf = Historical_Figure.query\
                          .filter_by(df_world_id=world_id, id=hfid)\
                          .first()
    pronoun = 'he' if hf.caste == 'MALE' else 'she'
    posessive = 'his' if hf.caste == 'MALE' else 'her'
    
    events = Historical_Event.query\
                             .filter(Historical_Event.df_world_id == world_id,
                                        or_(Historical_Event.hfid==hfid, 
                                            Historical_Event.hfid2==hfid))\
                             .limit(250).offset(evt_after)

    return render_template('histfig_detail.html', hf=hf, 
                           pronoun=pronoun, posessive=posessive,
                           events=events, rendered_events=[])
