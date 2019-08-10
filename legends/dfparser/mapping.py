db_names = {}

extract_values = lambda xml_dict: {k:v[0] for k, v in xml_dict.items()}


class Mapping(object):

    masked_fields = []
    mask_all = False
    
    def __init__(self, xml_dict, obj_name, world_id):
        self.xml_dict = xml_dict
        self.obj_name = obj_name
        self.world_id = world_id
        self.db_dicts = {}

    def get_db_mappings(self):
        '''

        Return the a dictionary containing all the db mappings
        created from this object.

        '''
        return self.db_dicts

    def convert(self):
        db_dict = extract_values(self.xml_dict) 
        db_dict['df_world_id'] = self.world_id
        self.db_dicts[self.obj_name] = [db_dict]

    def convert_detail(self, name, detail_dict_list, 
                       *rewrite_list, **parent_keys):
        for old, new in rewrite_list:
            for detail_dict in detail_dict_list:
                detail_dict[new] = detail_dict.pop(old, None)
        self.db_dicts[name] = [{**extract_values(detail_dict),
            'df_world_id' : self.world_id, **parent_keys}
            for detail_dict in detail_dict_list]

    def convert_list(self, detail_name, detail_list, 
            detail_key=None, **parent_keys):
        if not detail_key:
            detail_key = detail_name
        entries = [{"df_world_id" : self.world_id,
                    detail_key : detail, **parent_keys}
                   for detail in detail_list]
        if not detail_name in self.db_dicts:
            self.db_dicts[detail_name] = entries 
        else:
            self.db_dicts[detail_name].extend(entries)
    
    def alias_key(self, dict_name, db_field_name, *alias_names):
        for db_dict in self.db_dicts[dict_name]:
            for alias_name in alias_names:
                alias_val = db_dict.get(alias_name)
                if alias_val:
                    db_dict[db_field_name] = alias_val

    def mask_fields(self):
        for table, field in self.masked_fields:
            db_dict = self.db_dicts.get(table)
            if db_dict:
                db_dict.pop(field, None)
        if self.mask_all:
            self.db_dicts[self.obj_name] = {}

class Artifact_Mapping(Mapping):
    
    def convert(self):
        super().convert()

        self.alias_key(self.obj_name, 'written_content_id', 
                       'page_written_content_id', 'writing_written_content_id')

class Site_Mapping(Mapping):

    def __init__(self, xml_dict, obj_name, world_id):
        super().__init__(xml_dict, obj_name, world_id)

    def convert(self):

        site_id = self.xml_dict['id'][0]
        structures = self.xml_dict.get('structure') or []
        self.convert_detail('structure', structures, site_id=site_id)
        for structure in structures:
            if not 'id' in structure:
                # we're not in plus mode
                break
            structure_id = structure['id'][0] 
            inhabitants = structure.get("inhabitant", [])
            self.convert_list("inhabitant", inhabitants, "hfid", 
                    site_id=site_id, structure_id=structure_id)
        
        super().convert()

        self.alias_key("structure", "local_id", "local_id", "id")

class Histfig_Mapping(Mapping):

    def convert(self):
        hfid = self.xml_dict['id'][0]
        
        # these ones are simple, multi-field, details
        simple_details = ['hf_skill', 'entity_link','site_link', 
                          'entity_position_link', 'entity_reputation']
        for detail_name in simple_details:
            detail = self.xml_dict.get(detail_name) or []
            self.convert_detail(detail_name, detail, hfid=hfid)

        # hf_link and relationship_profile_hf_visual require changing
        # the name of the other hf for the db.
        hf_links = self.xml_dict.get('hf_link', [])
        self.convert_detail('hf_link', hf_links, ('hfid', 'hfid2'), 
                            hfid1=hfid)
        hf_rel_profs = self.xml_dict.get('relationship_profile_hf_visual', 
                                         [])
        self.convert_detail('relationship_profile_hf_visual', hf_rel_profs,
                            ('hf_id', 'hfid2'), hfid1=hfid)

        # these ones are single values, of which there may be more than
        # one for a given histfig
        one_field_details = ['sphere', 'goal', 'journey_pet', 
                             'interaction_knowledge']
        for detail_name in one_field_details:
            detail_list = self.xml_dict.get(detail_name) or []
            self.convert_list(detail_name, detail_list, hfid=hfid)
        
        super().convert()

class Eventcol_Mapping(Mapping):

    def convert(self):
        evtcol_id = self.xml_dict['id'][0]

        evtcols = self.xml_dict.get('eventcol') or []
        self.convert_list('eventcol_eventcol_link', evtcols, 'eventcol_id2',
                eventcol_id1=evtcol_id)
        evts = self.xml_dict.get('event') or []
        self.convert_list('eventcol_event_link', evts, 'event_id',
                eventcol_id=evtcol_id)
        hf_fields = ['attacking_hfid', 'defending_hfid', 'noncom_hfid']
        for hf_field in hf_fields:
            hfs = self.xml_dict.get(hf_field) or []
            self.convert_list(hf_field, hfs, 'hfid', eventcol_id=evtcol_id)

        # Squads are tricky. Each is represented by five fields, but they're
        # simply listedi in the XML, without being part of a sub-element of 
        # event collection. We need to do a little mask-and-zip trick
        # trick to make it fit the pattern the rest of the data takes. 

        squad_fields = ["_race", "_entity_pop", "_number", "_deaths", "_site"]
        squad_sides = ["attacking_squad", "defending_squad"]
        for side in squad_sides:
            side_fields = [side + field for field in squad_fields]
            squads = [self.xml_dict.get(field, []) for field in side_fields]
            zipped_squads = zip(*squads)
            squad_dicts = [{key : [squad[i]] for i, key in enumerate(side_fields)}
                           for squad in zipped_squads]
            self.convert_detail(side, squad_dicts, eventcol_id=evtcol_id) 

        super().convert()

        self.alias_key(self.obj_name, 'entity_id',
                  'entity_id', 'civ_id', 'attacking_enid')
        self.alias_key(self.obj_name, 'entity_id2',
                'entity_id2', 'defending_enid')

class Historical_Event_Mapping(Mapping):

    def convert(self):

        self.convert_list('competitor_hfid', 
                          self.xml_dict.get('competitor_hfid', []),
                          event_id=self.xml_dict['id'][0])

        super().convert()

        self.alias_key(self.obj_name, 'hfid', 'hfid', 'hist_figure_id', 
                       'giver_hist_figure_id', 'attacker_general_hfid', 
                       'group_1_hfid', 'spotter_hfid')
        self.alias_key(self.obj_name, 'hfid2', 'hfid2', 'hfid_target', 
                       'receiver_hist_figure_id', 'defender_general_hfid',
                       'group_2_hfid')
        self.alias_key(self.obj_name, 'entity_id', 'entity_id', 
                       'giver_entity_id', 'attacker_civ_id', 'civ_id', 
                       'attacker', 'entity_id_1')
        self.alias_key(self.obj_name, 'entity_id2', 'entity_id2',
                       'receiver_entity_id', 'defender_civ_id', 
                       'defender', 'involved', 'entity_id_2')
        self.alias_key(self.obj_name, 'building', 'building', 'building_id')
        self.alias_key(self.obj_name, 'site_id', 'site_id', 'site_id1')
        self.alias_key(self.obj_name, 'site_id2', 'site_id2', 'site_id_2')


class Written_Content_Mapping(Mapping):

    def convert(self):
        wc_id = self.xml_dict['id'][0]

        self.db_dicts['style'] = []
        for long_style in self.xml_dict.get('style') or []:
            style, magnitude = long_style.split(':') 
            style_dict = {'df_world_id':self.world_id, 'content_id':wc_id,
                'style':style, 'magnitude':magnitude}
            self.db_dicts['style'].append(style_dict)

        super().convert()

class Entity_Mapping(Mapping):

    masked_fields = [('structure', 'name')]

    def convert(self):
        entity_id = self.xml_dict['id'][0]

        entity_links = self.xml_dict.get('entity_link', [])
        self.convert_detail('entity_entity_link', entity_links, 
                            entity_id=entity_id)
        members = self.xml_dict.get('histfig_id', [])
        self.convert_list('member', members, 'hfid', entity_id=entity_id)

        entity_positions = self.xml_dict.get('entity_position', [])
        self.convert_detail('entity_position', entity_positions,
                entity_id=entity_id)

        e_p_as = self.xml_dict.get('entity_position_assignment', [])
        self.convert_detail('entity_position_assignment', e_p_as,
                entity_id=entity_id)

        occasions = self.xml_dict.get('occasion', [])
        self.convert_detail('occasion', occasions, entity_id=entity_id)
        for occasion in occasions:
            occasion_id = occasion['id'][0]
            schedules = occasion.get('schedule', [])

            self.convert_detail('schedule', schedules, entity_id=entity_id,
                                occasion_id=occasion_id)
            for schedule in schedules:
                schedule_id = schedule['id'][0]
                features = schedule.get('feature', [])
                self.convert_detail('feature', features, 
                                    entity_id=entity_id, 
                                    occasion_id=occasion_id,
                                    schedule_id=schedule_id)
        super().convert()

class Entity_Pop_Mapping(Mapping):

    def convert(self):
        long_race = self.xml_dict.get('race')
        if long_race:
            race, number = long_race[0].split(':')
            self.xml_dict['race'] = [race]
            self.xml_dict['num'] = [number]
        super().convert()

class Mapping_Factory(object):
    mapping_by_name = { "written_content" : Written_Content_Mapping,
                        "artifact" : Artifact_Mapping,
                        "site" : Site_Mapping,
                        "historical_figure" : Histfig_Mapping,
                        "historical_event_collection" : Eventcol_Mapping,
                        "historical_event" : Historical_Event_Mapping,
                        "entity" : Entity_Mapping,
                        "entity_population" : Entity_Pop_Mapping}

    def __init__(self, world_id):
        self.world_id = world_id

    def from_dict(self, name, xml_dict):
        return self.mapping_by_name.get(name, Mapping)(xml_dict, 
                                                       name, self.world_id)
