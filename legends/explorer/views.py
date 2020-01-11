from flask import Blueprint, render_template, request, url_for, jsonify

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, load_only

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

@bp.route('/api/<world_id>/events')
def events_json(world_id):
    q = (Historical_Event.query.filter(Historical_Event.df_world_id == world_id)
                               .options(joinedload(Historical_Event.hf).load_only('name'), 
                                       joinedload(Historical_Event.hf2).load_only('name'))
                               .order_by(Historical_Event.id))

    hf = request.args.get('hf')
    if hf:
        q = q.filter(or_(Historical_Event.hfid == hf, Historical_Event.hfid2 == hf))
    entity = request.args.get('entity')
    if entity:
        q = q.filter(or_(Historical_Event.entity_id == entity, Historical_Event.entity_id2 == entity))
    q=q.limit(250)
    
    events = [{
            'id':e.id,
            'year':e.year,
            'seconds72':e.seconds72,
            'type':e.type,
            'hfid':e.hfid,
            'hfid2':e.hfid2,
            'hf_name':titlecase(e.hf.name) if e.hf else None,
            'hf_name2':titlecase(e.hf2.name) if e.hf2 else None
            } for e in q.all()]

    return jsonify(events)

@bp.route('/api/<world_id>/histfig/<hfid>')
def hf_detail_json(world_id, hfid):
    hf = (Historical_Figure.query
                           .filter_by(df_world_id=world_id, id=hfid)
                           .options(joinedload(Historical_Figure.entity_links)
                                              .joinedload(Entity_Link.entity)
                                              .load_only('name'),
                                   joinedload(Historical_Figure.goals),
                                   joinedload(Historical_Figure.spheres))
                           .first())

    hf_links_q = (HF_Link.query
                       .filter_by(df_world_id=world_id, hfid1=hfid)
                       .options(joinedload(HF_Link.other)
                                          .load_only('name', 'birth_year',
                                                     'death_year', 'caste'))
                       )
                                 

    pronoun, posessive = hf.pronouns()
    
    entity_links = [{'entity_name':titlecase(el.entity.name), 
                     'entity_id':el.entity_id, 
                     'type':el.link_type} 
                     for el in hf.entity_links]
    
    hf_links = [{'hf_name':titlecase(link.other.name),
                 'birth_year':link.other.birth_year,
                 'death_year':link.other.death_year,
                 'caste':link.other.caste,
                 'hfid':link.hfid2,
                 'type':link.link_type
                } for link in hf_links_q]

    context = { 
                'name':titlecase(hf.name),
                'race':hf.race,
                'deity':hf.deity,
                'force':hf.force,
                'caste':hf.caste,
                'birth_year':hf.birth_year,
                'death_year':hf.death_year,
                'goals':[goal.goal for goal in hf.goals],
                'spheres':[sphere.sphere for sphere in hf.spheres],
                'entity_links':entity_links,
                'hf_links':hf_links,
                'pronoun':pronoun, 
                'posessive':posessive,
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

@bp.route('/api/<world_id>/entity/<entity_id>')
def entity_detail_json(world_id, entity_id):
    entity = (Entity.query
                     .filter_by(df_world_id=world_id, id=entity_id)
                     .first())
    entity_links = [{
        'link_type' : link.type,
        'entity_type' : link.forward_entity.type,
        'entity_name' : titlecase(link.forward_entity.name or "untitled"),
        'entity_id' : link.target
        } for link in entity.entity_links_out]


    entity_positions = [{
        'name' : position.calculated_name(),
        'vacant' : position.holder.histfig == -1 if position.holder else True,
        'hf_name' : titlecase(position.holder.hf.name) if position.holder.hf else None,
        'hfid' : position.holder.histfig if position.holder else None
        } for position in entity.positions]

    sites = [{
        'name' : titlecase(site.name),
        'id' : site.id,
        'type' : site.type
        } for site in entity.sites] 

    occasions = [{
        'name' : titlecase(occasion.name),
        'id' : occasion.id,
        } for occasion in entity.occasions] 

    context = {
            'name' : titlecase(entity.name or 'Untitled'),
            'type' : entity.type,
            'race' : entity.race,
            'entity_links' : entity_links,
            'entity_positions' : entity_positions,
            'sites' : sites,
            'occasions' : occasions
            }
    return jsonify(context)


@bp.route('/api/<world_id>/artifact/<artifact_id>')
def artifact_detail_json(world_id, artifact_id):
    artifact = (Artifact.query
                     .filter_by(df_world_id=world_id, id=artifact_id)
                     .first())

    written_content = {
            'title' : artifact.written_content.title,
            'form' : artifact.written_content.form,
            'author_name' : titlecase(artifact.written_content.author.name),
            'author_hfid' : artifact.written_content.author_hfid, 
            'styles' : artifact.written_content.style_string(),
            'subj_hf' : [(hf.name, hf.id) for hf in  artifact.written_content.referenced_hfs]
            } if artifact.written_content else None

    context = {
            'name' : titlecase(artifact.name),
            'item_type' : artifact.item_type,
            'mat' : artifact.mat,
            'written_content' : written_content
            }
    return jsonify(context)


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
