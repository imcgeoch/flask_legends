from flask import Blueprint, render_template, request, url_for, jsonify

from sqlalchemy import or_

from titlecase import titlecase

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
    return str([(world.id, world.name, world.altname) for world in worlds])

@bp.route('/api/hello')
def api_hello():
    return jsonify({'greeting':'hello, api'})

@bp.route('/<world_id>/histfigs')
def hf_index(world_id):
    after = request.args.get('after') or 0
    hfs = Historical_Figure.query\
                           .filter_by(df_world_id=world_id)\
                           .limit(250).offset(after)

    return render_template('histfig_list.html', items=hfs, context={})

@bp.route('/<world_id>/histfig/<hfid>')
def hf_detail(world_id, hfid):
    evt_after = request.args.get('evt_after') or 0
    hf = Historical_Figure.query\
                          .filter_by(df_world_id=world_id, id=hfid)\
                          .first()
    pronoun, posessive = hf.pronouns()
    events = hf.all_events
    context = { 'hf':hf, 'pronoun':pronoun, 'posessive':posessive, 
                'all_events':hf.all_events}

    return render_template('histfig_detail.html', hf=hf, 
                           pronoun=pronoun, posessive=posessive,
                           events=events, rendered_events=[], context=context)
@bp.route('/api/<world_id>/histfig/<hfid>')
def hf_detail_json(world_id, hfid):
    hf = Historical_Figure.query\
                          .filter_by(df_world_id=world_id, id=hfid)\
                          .first()
    pronoun, posessive = hf.pronouns()
    entity_links = [{'entity_name':titlecase(el.entity.name), 
                     'entity_id':el.entity_id, 
                     'type':el.link_type} 
                     for el in hf.entity_links]
    events = [{
        'type':event.type,
        'id':event.id,
        'hf_name':event.hf.name if event.hf else None,
        'hf_name2':event.hf2.name if event.hf2 else None,
        'hfid':event.hfid,
        'hfid2':event.hfid2
        } for event in hf.all_events]
    context = { 
                'name':titlecase(hf.name),
                'goals':[goal.goal for goal in hf.goals],
                'entity_links':entity_links,
                'pronoun':pronoun, 
                'posessive':posessive, 
                'events':events
              } 
    return jsonify(context)

@bp.route('/<world_id>/entities')
def entity_list(world_id):
    after = request.args.get('after') or 0
    entities = Entity.query\
                     .filter_by(df_world_id=world_id)\
                     .limit(250).offset(after)

    return render_template('entity_list.html', items=entities)

@bp.route('/<world_id>/entity/<entity_id>')
def entity_detail(world_id, entity_id):
    context = {}
    evt_after = request.args.get('evt_after') or 0
    context['entity'] = Entity.query\
                              .filter_by(df_world_id=world_id, id=entity_id)\
                              .first()
    return render_template('entity_detail.html', context=context)


@bp.route('/<world_id>/artifact/<artifact_id>')
def artifact_detail(world_id, artifact_id):
    context = {}
    evt_after = request.args.get('evt_after') or 0
    context['artifact'] = Artifact.query\
                              .filter_by(df_world_id=world_id, id=artifact_id)\
                              .first()
    return render_template('artifact_detail.html', context=context)


@bp.route('/<world_id>/artifacts')
def artifact_list(world_id):
    after = request.args.get('after') or 0
    artifacts = Artifact.query\
                     .filter_by(df_world_id=world_id)\
                     .limit(250).offset(after)

    return render_template('artifact_list.html', items=artifacts)

@bp.route('/<world_id>/occasion/<entity_id>/<occasion_id>')
def occasion_detail(world_id, entity_id, occasion_id):
    return "placeholder for occasion %s of entity %s" % (occasion_id, entity_id)

@bp.route('/<world_id>/site/<site_id>')
def site_detail(world_id, site_id):
    return "placeholder for site %s" % (site_id)

@bp.route('/<world_id>/region/<region_id>')
def region_detail(world_id, region_id):
    return "placeholder for region %s" % (region_id)
