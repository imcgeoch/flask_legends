import codecs
from xml.sax.handler import ContentHandler
from xml.sax import parse as sax_parse

from .connector import Connector
from .mapping import Mapping_Factory
from ..models import db

#from .. import create_app


def parse(filename, mode, world_id):

    app = create_app()
    app.app_context().push()

    if mode == 'insert':
        connector = Connector(db, 'insert', world_id)
        connector.add_world()
    elif mode == 'update':
        connector = Connector(db, 'update', world_id)
        
    factory = Mapping_Factory(world_id)

    with codecs.open(filename, 'r', encoding='CP437') as infile:
        sax_parse(infile, DF_Handler(connector, factory))


class DF_Handler(ContentHandler):
    stack = []
    namestack = []
    name = ''
    text = ''
    
    parentFieldNames = {"artifact", "region", "underground_region",
            "site", "historical_figure", "entity_population", "entity",
            "historical_event", "historical_event_collection", 
            "historical_era", "written_content", "poetic_form", 
            "musical_form", "dance_form",
            # begin plus 
            "landmass", "mountain_peak", "world_construction",
            "entity_population"}
    childFieldNames = {"structure", "entity_link", "hf_skill", "hf_link",
                       "site_link","entity_reputation", 
                       "entity_position_link", 
                       "relationship_profile_hf_visual",
                       "relationship_profile_hf_historical",
                       "vague_relationship",
                       # begin plus
                       "entity_position", "entity_position_assignment",
                       "occasion", "schedule", "feature", "reference"
                       }

    exclusiveChildren = {"reference" : "written_content"}

    allFieldNames = parentFieldNames.union(childFieldNames)

    def __init__(self, connector, factory):
        super().__init__()
        self.connector = connector
        self.factory = factory

    def startElement(self, name, attr):
        if name in self.allFieldNames:
            self.stack.append({})
            self.namestack.append(name)

        self.name = name 
        self.text = ''

    def endElement(self, tag):
        if len(self.stack) > 0:
            if tag in self.allFieldNames:
                self.namestack.pop()
            if tag in self.parentFieldNames and len(self.stack) == 1:
                mapping = self.factory.from_dict(tag, self.stack.pop())
                self.connector.add_mapping(mapping)
            else:
                if tag in self.childFieldNames:
                    val = self.stack.pop()
                    if tag in self.exclusiveChildren and self.namestack[-1] != self.exclusiveChildren[tag]:
                        val = self.text.replace("_", " ") or True
                else:
                    val = self.text.replace("_", " ") or True
                if tag in self.parentFieldNames:
                    self.stack.pop()
                top = self.stack[-1]
                top[tag] = (top.get(tag) or []) + [val]

        self.text = ''
    
    def characters(self, content):
        self.text += content
    def endDocument(self):
        self.connector.mappings_to_db()
