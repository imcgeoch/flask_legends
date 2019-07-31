import codecs
from xml.sax.handler import ContentHandler
from xml.sax import parse as sax_parse

from .connector2 import Connector
from .mapping import Mapping_Factory
from ..models import db

from .. import create_app


def parse(filename, mode, world_id):

    app = create_app()
    app.app_context().push()

    connector = Connector(db, 'insert', world_id)
    factory = Mapping_Factory(world_id) 
    
    with codecs.open(filename, 'r', encoding='CP437') as infile:
        sax_parse(infile, DF_Handler(connector, factory))


class DF_Handler(ContentHandler):
    stack = []
    name = ''
    text = ''
    ''' 
    parentFieldNames = {"artifact", "region", "underground_region",
            "site", "historical_figure", "entity_population", "entity",
            "historical_event", "historical_event_collection", 
            "historical_era", "written_content", "poetic_form", 
            "musical_form", "dance_form"}
    childFieldNames = {"structure", "entity_link", "hf_skill", "hf_link",
                       "site_link","entity_reputation", 
                       "entity_position_link", "relationship_profile_hf_visual"}
    '''
    parentFieldNames = {"artifact", "written_content", "site"}
    childFieldNames = {"structure"}

    allFieldNames = parentFieldNames.union(childFieldNames)

    def __init__(self, connector, factory):
        super().__init__()
        self.connector = connector
        self.factory = factory

    def startElement(self, name, attr):
        if name in self.allFieldNames:
            self.stack.append({})
        self.name = name 
        self.text = ''

    def endElement(self, tag):
        if len(self.stack) > 0:
            if tag in self.parentFieldNames:
                mapping = self.factory.from_dict(tag, self.stack.pop())
                self.connector.add_mapping(mapping)
            else:
                val = self.stack.pop() if (tag in self.childFieldNames) \
                                    else self.text or True 
                top = self.stack[-1]
                top[tag] = (top.get(tag) or []) + [val]

        self.text = ''
    
    def characters(self, content):
        self.text += content

    def endDocument(self):
        self.connector.convert_and_insert_mappings()
