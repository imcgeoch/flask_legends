from flask import Blueprint, render_template, request, url_for, jsonify

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, load_only

from titlecase import titlecase

from os import path

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

@bp.route('/api/<world_id>')
def api_world(world_id):
    world = DF_World.query.get(world_id)

    return jsonify({'name':titlecase(world.name),
                    'altname': world.altname})

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
        'vacant' : not position.holder.hf if position.holder else True,
        'hf_name' : titlecase(position.holder.hf.name) if position.holder and position.holder.hf else None,
        'hfid' : position.holder.histfig if position.holder else None
        } for position in entity.positions] 
    sites = [{
        'name' : titlecase(site.name),
        'id' : site.id,
        'type' : site.type
        } for site in entity.sites + entity.local_sites] 

    occasions = [{
        'name' : titlecase(occasion.name),
        'id' : occasion.id,
        'entityid' : entity_id,
        'worldid' : world_id
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


@bp.route('/api/<world_id>/written_content/<wc_id>')
def wc_detail_json(world_id, wc_id):
    wc = (Written_Content.query
            .filter_by(df_world_id=world_id, id=wc_id)
            .first())
    
    written_content = {
            'wc_id' : wc.id,
            'title' : wc.title,
            'form' : wc.form,
            'author_name' : titlecase(wc.author.name),
            'author_hfid' : wc.author_hfid, 
            'styles' : wc.style_string(),
            'subj_hf' : [{'hf_name' : titlecase(hf.name), 'hfid' : hf.id} 
                         for hf in  wc.referenced_hfs],
            'subj_evt' : [{
                            'id':e.id,
                            'year':e.year,
                            'seconds72':e.seconds72,
                            'type':e.type,
                            'hfid':e.hfid,
                            'hfid2':e.hfid2,
                            'hf_name':titlecase(e.hf.name) if e.hf else None,
                            'hf_name2':titlecase(e.hf2.name) if e.hf2 else None
                           } for e in wc.referenced_events],
            'subj_site' : [{'name' : titlecase(site.name),
                            'id' : site.id}
                         for site in  wc.referenced_sites],
            'subj_artifact' : [{'name' : afct.name, 'id' : afct.id} 
                         for afct in  wc.referenced_artifacts],
            'subj_entity' : [{'name' : entity.name, 'id' : entity.id} 
                         for entity in  wc.referenced_entities],
            'subj_region' : [{'name' : region.name, 'id' : region.id} 
                         for region in  wc.referenced_regions],
            'subj_wc' : [{'wc_id' : swc.id, 'wc_name' : swc.title,
                          'linking_wc_id' : wc.id, 'worldid' : world_id} 
                         for swc in  wc.referenced_wcs],
            'subj_poetic' : [{'name' : poetic.name, 'id':poetic.id} 
                         for poetic in  wc.referenced_poetic_forms],
            'subj_dance' : [{'name' : dance.name, 'id' : dance.id} 
                         for dance in  wc.referenced_dance_forms],
            'subj_musical' : [{ 'name' : musical.name, 'id' : musical.id} 
                         for musical in  wc.referenced_musical_forms]
            } 
    return jsonify(written_content)

@bp.route('/api/<world_id>/artifact/<artifact_id>')
def artifact_detail_json(world_id, artifact_id):
    artifact = (Artifact.query
                     .filter_by(df_world_id=world_id, id=artifact_id)
                     .first())

    written_content = {
            'wc_id' : artifact.written_content.id,
            'wc_name' : artifact.written_content.title
            } if artifact.written_content else None

    holder = {
            'hf_name' : titlecase(artifact.holder_hf.name),
            'hfid' : artifact.holder_hf.id,
            'worldid' : artifact.holder_hf.df_world_id
            } if artifact.holder_hf else None
    site = {
            'name' : titlecase(artifact.storage_site.name),
            'id' : artifact.storage_site.id,
            'worldid' : artifact.storage_site.df_world_id
            } if artifact.storage_site else None

    context = {
            'name' : titlecase(artifact.name or "Untitled"),
            'name_string' : titlecase(artifact.name_string or ""),
            'item_type' : artifact.item_subtype or artifact.item_type,
            'mat' : artifact.mat,
            'written_content' : written_content,
            'item_description' : artifact.item_description,
            'holder' : holder,
            'site' : site
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

@bp.route('/api/<world_id>/occasion/<entity_id>/<occasion_id>')
def occasion_detail_json(world_id, entity_id, occasion_id):
    occasion = (Occasion.query
                            .filter_by(df_world_id=world_id, 
                                       entity_id=entity_id,
                                       id=occasion_id)
                            .first())
    def feature_dict(feature):
        musical_form = feature.referenced_musical_form
        dance_form = feature.referenced_dance_form
        poetic_form = feature.referenced_poetic_form
        e = feature.referenced_event
        context = {
                'type' : feature.type,
                'musical_form' : { 
                    "name" : musical_form.name,
                    "id" : musical_form.id,
                    "worldid" : world_id
                    } if musical_form else None,
                'dance_form' : { 
                    "name" : dance_form.name,
                    "id" : dance_form.id,
                    "worldid" : world_id
                    } if dance_form else None,
                'poetic_form' : { 
                    "name" : poetic_form.name,
                    "id" : poetic_form.id,
                    "worldid" : world_id
                    } if poetic_form else None,
                "event" : {
                        'id':e.id,
                        'year':e.year,
                        'seconds72':e.seconds72,
                        'type':e.type,
                        'hfid':e.hfid,
                        'hfid2':e.hfid2,
                        'hf_name':titlecase(e.hf.name) if e.hf else None,
                        'hf_name2':titlecase(e.hf2.name) if e.hf2 else None
                        } if e else None,
                #//also references a la written content
                }
        return context

    def schedule_dict(schedule):
        musical_form = schedule.referenced_musical_form
        dance_form = schedule.referenced_dance_form
        poetic_form = schedule.referenced_poetic_form
        e = schedule.referenced_event

        context = {
                'type' : schedule.type,
                'item_subtype' : schedule.item_subtype,
                'features' : [feature_dict(feature)
                              for feature in schedule.features],
                'musical_form' : { 
                    "name" : musical_form.name,
                    "id" : musical_form.id,
                    "worldid" : world_id
                    } if musical_form else None,
                'dance_form' : { 
                    "name" : dance_form.name,
                    "id" : dance_form.id,
                    "worldid" : world_id
                    } if dance_form else None,
                'poetic_form' : { 
                    "name" : poetic_form.name,
                    "id" : poetic_form.id,
                    "worldid" : world_id
                    } if poetic_form else None,
                "event" : {
                        'id':e.id,
                        'year':e.year,
                        'seconds72':e.seconds72,
                        'type':e.type,
                        'hfid':e.hfid,
                        'hfid2':e.hfid2,
                        'hf_name':titlecase(e.hf.name) if e.hf else None,
                        'hf_name2':titlecase(e.hf2.name) if e.hf2 else None,
                        'worldid':world_id
                        } if e else None,
                }

        return context

    e = occasion.historical_event

    context = {
            "entity_name" : titlecase(occasion.entity.name),
            "name" : occasion.name,
            "event" : {
                        'id':e.id,
                        'year':e.year,
                        'seconds72':e.seconds72,
                        'type':e.type,
                        'hfid':e.hfid,
                        'hfid2':e.hfid2,
                        'hf_name':titlecase(e.hf.name) if e.hf else None,
                        'hf_name2':titlecase(e.hf2.name) if e.hf2 else None
                        } if e else None,
            'schedules' : [schedule_dict(schedule) 
                           for schedule in occasion.schedules]
            }

    return jsonify(context)

@bp.route('/api/<world_id>/site/<site_id>')
def site_detail_json(world_id, site_id):
    site = (Site.query
                     .filter_by(df_world_id=world_id, id=site_id)
                     .first())
    civ = {
            "entity_name" : titlecase(site.entity.name),
            "entity_id" : site.entity.id,
            "worldid" : site.entity.df_world_id
            } if site.entity else None

    site_gvt = {
            "entity_name" : titlecase(site.local_entity.name),
            "entity_id" : site.local_entity.id,
            "worldid" : site.local_entity.df_world_id
            } if site.local_entity else None

    img_filename = 'img/%s/site%s.png' % (world_id, site_id)
    img = url_for('explorer.static', filename=img_filename) \
            if path.exists('./legends/explorer/static/' + img_filename) else None

    structures = [{
        "name" : structure.name,
        "name_2" : structure.name2,
        "type" : structure.type,
        "subtype" : structure.subtype,
        "worship_hf" : {
            "hf_name" : titlecase(structure.historical_figure.name or ""),
            "hfid" : structure.historical_figure.id,
            "worldid" : world_id
            } if structure.historical_figure else None,
        } for structure in site.structures]

    context = {
            "name" : titlecase(site.name),
            "type" : site.type,
            "civ" : civ,
            "site_gvt" : site_gvt,
            "img" : img,
            "structures" : structures
            }

    return jsonify(context)

@bp.route('/api/<world_id>/musicalform/<form_id>')
def musical_form_detail_json(world_id, form_id):
    form = (Musical_Form.query
                     .filter_by(df_world_id=world_id, id=form_id)
                     .first())
    context = {
            "name" : form.name,
            "description" : form.description
            }
    

    return jsonify(context)

@bp.route('/api/<world_id>/danceform/<form_id>')
def dance_form_detail_json(world_id, form_id):
    form = (Dance_Form.query
                     .filter_by(df_world_id=world_id, id=form_id)
                     .first())
    context = {
            "name" : form.name,
            "description" : form.description
            }
    

    return jsonify(context)

@bp.route('/api/<world_id>/poeticform/<form_id>')
def poetic_form_detail_json(world_id, form_id):
    form = (Poetic_Form.query
                     .filter_by(df_world_id=world_id, id=form_id)
                     .first())
    context = {
            "name" : form.name,
            "description" : form.description
            }
    

    return jsonify(context)

@bp.route('/<world_id>/site/<site_id>')
def site_detail(world_id, site_id):
    return "placeholder for site %s" % (site_id)

@bp.route('/<world_id>/region/<region_id>')
def region_detail(world_id, region_id):
    return "placeholder for region %s" % (region_id)

@bp.route('/api/<world_id>/eventcollection/<evtcol_id>')
def evtcol_detail(world_id, evtcol_id):
    evtcol = Event_Collection.query.get((world_id, evtcol_id))

    def duel_context(evtcol):
        context = {
                "type" : evtcol.type,
                "battle" : evtcol_context(evtcol.linking_collections[0]),
                "start_year" : evtcol.start_year,
                "events" : [event_context(event) 
                            for event in evtcol.linked_events]
                }
        return context

    def evtcol_context(evtcol):
        context = {
                "name" : titlecase(evtcol.name or ""),
                "id" : evtcol.id,
                "worldid" : evtcol.df_world_id,
                "type" : evtcol.type
                }
        
        return context

    def hf_context(hf):
        context = {
                "hf_name" : titlecase(hf.name),
                "hfid" : hf.id,
                "worldid" : hf.df_world_id
                }
        return context

    def site_context(site):
        context = {
                "name" : titlecase(site.name),
                "id" : site.id,
                "worldid" : site.df_world_id
                }
        return context

    def squad_context(squad, side):
        context = {
                "race" : squad.attacking_squad_race if side == "attacking"
                         else squad.defending_squad_race,
                "number" : squad.attacking_squad_number if side == "attacking"
                         else squad.defending_squad_number,
                "deaths" : squad.attacking_squad_deaths if side == "attacking"
                         else squad.defending_squad_deaths,
                "site" : site_context(squad.site) if squad.site else None
                }
        return context

    def battle_context(evtcol):
        context = {
                "id" :  evtcol.id,
                "worldid" : evtcol.df_world_id,
                "type" : evtcol.type,
                "name" : titlecase(evtcol.name or ""),
                "start_year" : evtcol.start_year,
                "end_year" : evtcol.start_year,
                "attacking_squads" : [squad_context(squad, 'attacking')
                                      for squad in evtcol.attacking_squads],
                "defending_squads" : [squad_context(squad, 'defending')
                                      for squad in evtcol.defending_squads],
                "attacking_hfs" : [hf_context(hf) for hf in evtcol.attackers],
                "defending_hfs" : [hf_context(hf) for hf in evtcol.defenders],
                "noncom_hfs" : [hf_context(hf) for hf in evtcol.noncoms],
                "events" : [event_context(event)
                            for event in evtcol.linked_events],
                "duels" : [evtcol_context(linked_col)
                             for linked_col in evtcol.linked_collections
                             if linked_col.type == 'duel'],
                "war" : evtcol_context(evtcol.linking_collections[0])
                }

        return context

    def event_context(event):
        context = {
                "id" : event.id,
                "year" : event.year,
                "type" : event.type
                }
        return context

    def entity_context(entity):
        context = {
                "entity_name" : titlecase(entity.name),
                "entity_id" : entity.id,
                "worldid" : entity.df_world_id
                } if entity else {}
        return context
        
    def war_context(evtcol):
        context = {
                "type" : evtcol.type,
                "name" : titlecase(evtcol.name or ""),
                "start_year" : evtcol.start_year,
                "end_year" : evtcol.end_year,
                "battles" : [evtcol_context(linked_col)
                             for linked_col in evtcol.linked_collections
                             if linked_col.type == 'battle'],
                "events" : [event_context(event)
                            for event in evtcol.linked_events],
                "aggressor" : entity_context(evtcol.entity1),
                "defender" : entity_context(evtcol.entity2),
                }

        return context

    def conquest_context(evtcol):
        context = {
                "type" : evtcol.type,
                "start_year" : evtcol.start_year,
                "events" : [event_context(event)
                            for event in evtcol.linked_events],
                "site" : site_context(evtcol.site),
                "aggressor" : entity_context(evtcol.entity1),
                "defender" : entity_context(evtcol.entity2),
                "war" : evtcol_context(evtcol.linking_collections[0])
                }
        return context

    def occasion_context(occasion):
        context = {
                "id" : occasion.id,
                "entityid" : occasion.entity_id,
                "worldid" : occasion.df_world_id,
                "name" : occasion.name
                }
        return context

    def occasion_evtcol_context(evtcol):
        context = {
                "type" : evtcol.type,
                "occasion" : occasion_context(evtcol.occasion),
                "start_year" : evtcol.start_year,
                "ordinal" : evtcol.ordinal,
                "schedules" : [evtcol_context(schedule)
                               for schedule in evtcol.linked_collections],
                "entity" : entity_context(evtcol.entity1)
                
                }
        return context

    def schedule_context(evtcol):
        context = {
                "type" : evtcol.type,
                "occasion" : evtcol_context(
                               evtcol.linking_collections[0]),
                "event" : event_context(evtcol.linked_events[0]),
                "year" : evtcol.start_year
                }
        return context

    def purge_context(evtcol):
        context = {
                "type" : evtcol.type,
                "adjective" : evtcol.adjective.lower(),
                "year" : evtcol.start_year,
                "site" : site_context(evtcol.site),
                "events" : [event_context(event) for 
                    event in evtcol.linked_events]
                }
        return context

    def journey_context(evtcol):
        context = {
                "type" : evtcol.type,
                "year" : evtcol.start_year,
                "ordinal" : evtcol.ordinal,
                "events" : [event_context(event) for
                    event in evtcol.linked_events]
                }
        return context

    def beast_attack_context(evtcol):
        context  = {
                "type" : evtcol.type,
                "year" : evtcol.start_year,
                "events" : [event_context(event) for
                    event in evtcol.linked_events],
                "evtcol" : (evtcol_context( evtcol.linking_collections[0]) 
                    if len_evtcol.linking_collections > 0 
                    else None),
                "site" : site_context(evtcol.site)
                }
        return context

    def theft_context(evtcol):
        context = {
                "type" : evtcol.type,
                "year" : evtcol.start_year,
                "events" : [event_context(event) for
                    event in evtcol.linked_events],
                "duels" : [evtcol_context(linked_col)
                             for linked_col in evtcol.linked_collections
                             if linked_col.type == 'duel'],
                }
        return context

    if evtcol.type == 'war':
        return jsonify(war_context(evtcol))
    if evtcol.type == 'battle':
        return jsonify(battle_context(evtcol))
    if evtcol.type == 'duel':
        return jsonify(duel_context(evtcol))
    if evtcol.type == 'site conquered':
        return jsonify(conquest_context(evtcol))
    if evtcol.type == 'occasion':
        return jsonify(occasion_evtcol_context(evtcol))
    if (evtcol.type == 'ceremony'
            or evtcol.type == 'procession'
            or evtcol.type == 'performance'
            or evtcol.type == 'competition'):
        return jsonify(schedule_context(evtcol))
    if evtcol.type == 'purge':
        return purge_context(evtcol)
    if evtcol.type == 'journey':
        return journey_context(evtcol)
    if evtcol.type == 'theft':
        return theft_context(evtcol)

    return jsonify({"type": evtcol.type})

