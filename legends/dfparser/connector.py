from ..models import *
from ..models.collections import eventcol_eventcol_link,\
                                 eventcol_event_link,\
                                 eventcol_attackers,\
                                 eventcol_defenders,\
                                 eventcol_noncoms

import pprint

class Connector():


     
    dicts = {}
    
    tables = {(Artifact, 'artifact'), (Region, 'region'),
            (Underground_Region, 'underground_region'), (Site, 'site'),
            (Structure, 'structure'),
            (Historical_Figure, 'historical_figure'), 
            (Skill, 'hf_skill'), (Entity_Link, 'entity_link'),
            (Sphere, 'sphere'), (Goal, 'goal'),
            (Journey_Pet, 'journey_pet'),
            (Interaction_Knowledge, 'interaction_knowledge'),
            (HF_Link, 'hf_link'), (Site_Link, 'site_link'),
            (Entity_Position_Link, 'entity_position_link'),
            (Entity_Reputation, 'entity_reputation'),
            (Relationship, 'relationship_profile_hf_visual'),
            (Entity_Population, 'entity_population'),
            (Entity, 'entity'), 
            (Historical_Event, 'historical_event'),
            (Event_Collection, 'historical_event_collection'),
            (Historical_Era, 'historical_era'),
            (Style, 'style'),
            (Written_Content, 'written_content'),
            (Poetic_Form, 'poetic_form'),
            (Musical_Form, 'musical_form'),
            (Dance_Form, 'dance_form')
            }
    aux_tables = {(eventcol_eventcol_link, 'evtcol_evtcol'),
                  (eventcol_event_link, 'evtcol_event'),
                  (eventcol_attackers, 'attacking_hfid'),
                  (eventcol_defenders, 'defending_hfid'),
                  (eventcol_noncoms, 'noncom_hfid')
                  }

    def __init__(self, db, mode, world_id):
        # takes a connection to our db
        self.db = db
        self.mode = mode
        self.world_id = world_id
        self.pp = pprint.PrettyPrinter()

        self.counter = 0
    
        self.update_fns = {'artifact':self.add_artifact, 
                  'region':self.add_simple, 
                  'underground_region':self.add_simple,
                  'site':self.add_site,
                  'historical_figure':self.add_histfig,
                  'entity_population':self.add_simple,
                  'entity':self.add_simple,
                  'historical_event':self.add_historical_event,
                  'historical_event_collection':self.add_evtcol,
                  'historical_era':self.add_simple,
                  'written_content':self.add_written_content,
                  'poetic_form':self.add_simple,
                  'musical_form':self.add_simple,
                  'dance_form':self.add_simple}
        self.hf_children = {('hf_skill', None),
                         ('entity_link', None),
                         ('site_link', None),
                         ('entity_position_link', None),
                         ('entity_reputation', None), 
                         ('hf_link', self.add_two_hf_child('hfid')),
                         ('relationship_profile_hf_visual',
                          self.add_two_hf_child('hf_id')),
                         ('sphere', self.make_add_hf_detail('sphere')),
                         ('goal', self.make_add_hf_detail('goal')),
                         ('journey_pet', 
                             self.make_add_hf_detail('journey_pet')),
                         ('interaction_knowledge',
                         self.make_add_hf_detail('interaction_knowledge'))}

    def add(self, name, mapping):
        # takes a dict mapping keys to fields 
        # from an xml parser, by calling appropriate helper
        #
        # converts to one or more ready-to insert dicts
        # 
        # calls bulk_insert_all if nessecary
        # (according to size or soemthing tbd)
        # print(name, mapping)

        self.update_dict(name, self.update_fns[name](mapping))
        self.counter = self.counter + 1
        if self.counter > 10000:
            self.counter = 0
            self.bulk_insert_all()


    def update_dict(self, name, mapping):
        if name in self.dicts:
            self.dicts[name] += mapping
        else:
            self.dicts[name] = mapping

    def bulk_insert_all(self):
        #
        # calls db.bulk_insert for each thing in dicts
        # then clears it out
        # print(self.dicts)

        s = self.db.session

        # TODO:
        # See if we can cause these to be split if they're too big
        for obj, key in self.tables:
            s.bulk_insert_mappings(obj, self.dicts.get(key) or {})
            self.dicts[key] = []
  
        for tab, key in self.aux_tables:
            s.execute(tab.insert(self.dicts.get(key)))
            self.dicts[key] = []
        #s.execute(eventcol_eventcol_link.insert(
        #self.dicts.get('evtcol_evtcol')))

        s.commit()

    def get_first(self, mapping):
        return {k:v[0] for k, v in mapping.items()}  

    def add_simple(self, mapping):
        mapping = self.get_first(mapping)
        mapping['df_world_id'] = self.world_id
        return [mapping]
    
    def add_artifact(self, mapping):
        mapping = self.add_simple(mapping)[0]
        mapping['written_content_id'] = \
            mapping.get('page_written_content_id') or \
            mapping.get('writing_written_contnet_id')
        return [mapping]

    def add_site(self, mapping):
        struc_map = mapping.get('structure') or [] 
        for m in struc_map:
            self.update_dict('structure', 
                             self.add_structure(m, mapping['id']))
        return self.add_simple(mapping)

    def add_structure(self, mapping, site):
        mapping = self.add_simple(mapping)[0]
        mapping['site_id'] = site[0]
        mapping['entity_id'] = mapping.get('entity_id') or -1
        return [mapping]
    
    def add_histfig(self, mapping):
        hfid = mapping['id'][0]

        for child_name, func in self.hf_children:
            func = func or self.add_hf_child
            children = mapping.get(child_name) or []
            for child in children:
                maps = func(child, hfid)
                self.update_dict(child_name, maps)
        
        return self.add_simple(mapping)

    def make_add_hf_detail(self, name):
        def f(item, hfid):
            mp = {'df_world_id':self.world_id, 'hfid':hfid, name:item} 
            return [mp]
        return f
     
    def add_two_hf_child(self, name):
        def f(mapping, hfid):
            mapping = self.add_simple(mapping)[0]
            mapping['hfid1'] = hfid
            mapping['hfid2'] = mapping[name]
            #mapping['rep'] = mapping.get('rep_buddy') # fix in db
            return [mapping]
        return f

    def add_hf_child(self, mapping, hfid):
        mapping = self.add_simple(mapping)[0]
        mapping['hfid'] = hfid
        return [mapping]

    def add_historical_event(self, mapping):
        mapping = self.add_simple(mapping)[0]

        # losts of aliases
        mapping['hfid'] = mapping.get('hfid') or\
                          mapping.get('hist_figure_id') or\
                          mapping.get('giver_hist_figure_id') or\
                          mapping.get('attacker_general_hfid') or\
                          mapping.get('group_1_hfid') or\
                          mapping.get('spotter_hfid')
        mapping['hfid2'] = mapping.get('hfid2') or\
                           mapping.get('hfid_target') or\
                           mapping.get('receiver_hist_figure_id') or\
                           mapping.get('defender_general_hfid') or\
                           mapping.get('group_2_hfid')
        mapping['entity_id'] = mapping.get('entity_id') or\
                               mapping.get('giver_entity_id') or\
                               mapping.get('attacker_civ_id') or\
                               mapping.get('civ_id') or\
                               mapping.get('attacker') or\
                               mapping.get('entity_id_1')
        mapping['entity_id2'] = mapping.get('receiver_entity_id') or\
                                mapping.get('defender_civ_id') or\
                                mapping.get('defender') or\
                                mapping.get('involved') or\
                                mapping.get('entity_id_2')
        mapping['building'] = mapping.get('building') or\
                              mapping.get('building_id')
        mapping['site_id'] = mapping.get('site_id') or\
                             mapping.get('site_id1')
        mapping['site_id2'] = mapping.get('site_id2') or\
                              mapping.get('site_id_2')
        
        return [mapping]

    def add_evtcol(self, mapping):
        evtcol_id = mapping['id'][0]

        # TODO : Squad

        # TODO : Refactor out redundency 

        for evtcol in mapping.get('eventcol') or []:
            mp = [{'df_world_id':self.world_id, 'eventcol_id1':evtcol_id,
                   'eventcol_id2':evtcol}]
            self.update_dict('evtcol_evtcol', mp)
        for event in mapping.get('event') or []:
            mp = [{'df_world_id':self.world_id, 'eventcol_id':evtcol_id,
                   'event_id':event}]
            self.update_dict('evtcol_event', mp)
        for col in ['attacking_hfid', 'defending_hfid', 'noncom_hfid']:
            for event in mapping.get(col) or []:
                mp = [{'df_world_id':self.world_id, 
                    'eventcol_id':evtcol_id, 'hfid':event}]
                self.update_dict(col, mp)
        mapping = self.add_simple(mapping)[0]

        mapping['entity_id'] = mapping.get('entity_id') or\
                               mapping.get('civ_id') or\
                               mapping.get('attacking_enid')
        mapping['entity_id2'] = mapping.get('entity_id2') or\
                                mapping.get('defending_enid')
       
        return [mapping]

    def add_written_content(self, mapping):
        wc_id = mapping['id'][0]

        for style in mapping.get('style') or []:
            style, magnitude = style.split(':') 
            mp = [{'df_world_id':self.world_id, 'content_id':wc_id,
                'style':style, 'magnitude':magnitude}]
            self.update_dict('style', mp)
        mapping = self.add_simple(mapping)[0]

        return [mapping]

