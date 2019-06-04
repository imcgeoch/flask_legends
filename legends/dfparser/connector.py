from ..models import Artifact

class Connector():

    dicts = {}

    def __init__(self, db, mode, world_id):
        # takes a connection to our db
        self.db = db
        self.mode = mode
        self.world_id = world_id

    def add(self, name, mapping):
        # takes a dict mapping keys to fields 
        # from an xml parser, by calling appropriate helper
        #
        # converts to one or more ready-to insert dicts
        # 
        # calls bulk_insert_all if nessecary
        # (according to size or soemthing tbd)
        print(name, mapping)

        if name == 'artifact':
            self.update_dict('artifacts', self.add_artifact(mapping))


    def update_dict(self, name, mapping):
        if name in self.dicts:
            self.dicts[name] += [mapping]
        else:
            self.dicts[name] = [mapping]

    def bulk_insert_all(self):
        #
        # calls db.bulk_insert for each thing in dicts
        # then clears it out
        print(self.dicts)
        s = self.db.session
        s.bulk_insert_mappings(Artifact, self.dicts['artifacts'])
        s.commit()

    def add_artifact(self, mapping):
        mapping['df_world_id'] = self.world_id
        mapping['written_content_id'] = \
            mapping.get('page_written_content_id') or \
            mapping.get('writing_written_contnet_id')
        return mapping

