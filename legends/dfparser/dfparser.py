import codecs
from xml.etree.ElementTree import iterparse, XMLParser
from xml.sax.handler import ContentHandler
from xml.sax import parse as sax_parse

from .connector import Connector

from ..models import db, DF_World, Artifact

from .. import create_app

def do_parse(fname1, fname2, worldname):
    world = DF_World(name=worldname)
    db.session.add(world)
    db.session.commit()
    world_id = world.id
    parse(fname1, "base")

def parse(filename, mode):

    app = create_app()
    app.app_context().push()

    # parser = XMLParser(encoding='CP437', target=DF_XMLParser())
    #itr = iterparse(filename, parser=parser)
    connector = Connector(db, 'insert', 1)
    with codecs.open(filename, 'r', encoding='CP437') as infile:
        #for line in infile:
        #    parser.feed(line)
        sax_parse(infile, DF_Handler(connector))


class DF_Handler(ContentHandler):
    stack = []
    name = ''
    text = ''
    
    parentFieldNames = {"artifact", "region", "underground_region",
            "site", "historical_figure"}
    childFieldNames = {"structure", "entity_link", "hf_skill", "hf_link",
                       "site_link","entity_reputation", 
                       "entity_position_link", "relationship_profile_hf_visual"}
    allFieldNames = parentFieldNames.union(childFieldNames)

    def __init__(self, connector):
        super().__init__()
        self.connector = connector


    def startElement(self, name, attr):
        # print("start " + name)
        if name in self.allFieldNames:
            self.stack.append({})
        self.name = name 
        self.text = ''

    def endElement(self, tag):
        if len(self.stack) > 0:
            if tag in self.parentFieldNames:
                self.connector.add(tag, self.stack.pop())
            else:
                val = self.stack.pop() if (tag in self.childFieldNames) \
                                    else self.text or True 
                top = self.stack[-1]
                top[tag] = (top.get(tag) or []) + [val]

            #elif tag in self.childFieldNames:
            #    child = self.stack.pop()
            #    self.stack[-1][tag] = self.stack[-1][tag] + [child] \
            #            or [child] 
            #else:
            #    self.stack[-1][tag] = self.text or True
        self.text = ''
    
    def characters(self, content):
        self.text += content

    def endDocument(self):
        self.connector.bulk_insert_all()

"""
class DF_XMLParser():
    stack = []
    name = ''
    text = ''

    parentFieldNames = {"artifact"}
    childFieldNames = {"item"}
    allFieldNames = parentFieldNames.union(childFieldNames)

    def start(self, tag, attrib):
        # print("start " + tag)
        if tag in self.allFieldNames:
            self.stack.append({})
        self.name = tag

    def end(self, tag):
        if len(stack > 0):
            if tag in self.parentFieldNames:
                print(tag, self.stack.pop())
            elif tag in self.childFieldNames:
                child = self.stack.pop()
                self.stack[-1][tag] = child 
            else:
                self.stack[-1][tag] = self.text or True
                self.text = ""
    
    def characters(content):
        self.text = content

    def data(self, data):
        # update string
        pass

    def close(self):
        pass
"""
