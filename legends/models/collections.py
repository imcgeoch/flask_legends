from . import db
from .join_builder import join_builder as jb, table_join_builder as tjb

## TODO : Squad!

eventcol_event_link = db.Table('eventcol_event_link', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('event_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        )
        

eventcol_eventcol_link = db.Table('eventcol_eventcol_link', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id1', db.Integer),
        db.Column('eventcol_id2', db.Integer),
        )

eventcol_attackers = db.Table('eventcol_attackers', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        )
eventcol_defenders = db.Table('eventcol_defenders', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        )
eventcol_noncoms = db.Table('eventcol_noncoms', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        )

class Event_Collection(db.Model):
    __tablename__ = 'event_collections'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    start_seconds72 = db.Column(db.Integer)
    end_seconds72 = db.Column(db.Integer)

    subregion_id = db.Column(db.Integer)
    coords       = db.Column(db.String(20))
    feature_layer_id = db.Column(db.Integer)
    
    name = db.Column(db.String(50))
    adjective = db.Column(db.String(50))
    type = db.Column(db.String(20))
    ordinal = db.Column(db.Integer)
    occasion_id = db.Column(db.Integer)

    site_id = db.Column(db.Integer)
    
    # Eventcol relations
    parent_eventcol = db.Column(db.Integer)
    war_eventcol = db.synonym(parent_eventcol)

    #Entity related
    entity_id = db.Column(db.Integer)
    entity_id2 = db.Column(db.Integer)

    civ_id = db.synonym(entity_id)
    attacking_enid = db.synonym(entity_id)
    defending_enid = db.synonym(entity_id2)

    children = db.relationship('Event_Collection', remote_side=[id], 
                               backref='parent', viewonly=True,
                               foreign_keys=[df_world_id, parent_eventcol],
                               primaryjoin=jb("Event_Collection",
                                              "Event_Collection",
                                              ("id", "parent_eventcol")))

    linked_collections = db.relationship('Event_Collection',
                                         secondary='eventcol_eventcol_link', 
                                         backref='linking_collections',
                                         viewonly=True,
                                         primaryjoin=tjb("Event_Collection", 
                                                     "eventcol_eventcol_link",
                                                     ("id", "eventcol_id1")),
                                         secondaryjoin=tjb("Event_Collection", 
                                                       "eventcol_eventcol_link",
                                                       ("id", "eventcol_id2")))

    linked_events = db.relationship('Historical_Event', 
                                     viewonly=True, 
                                     secondary='eventcol_event_link',
                                     backref='collections',
                                     primaryjoin=tjb("Event_Collection", 
                                                 "eventcol_event_link",
                                                 ("id", "eventcol_id")),
                                     secondaryjoin=tjb("Historical_Event", 
                                                   "eventcol_event_link",
                                                   ("id", "event_id")))

    attackers = db.relationship('Historical_Figure', 
                                viewonly=True,
                                secondary='eventcol_attackers',
                                backref='attacker_collections',
                                primaryjoin=tjb("Event_Collection", 
                                                "eventcol_attackers",
                                                ("id", "eventcol_id")),
                                secondaryjoin=tjb("Historical_Figure", 
                                                  "eventcol_attackers",
                                                  ("id", "hfid")))

    defenders = db.relationship('Historical_Figure', 
                                viewonly=True,
                                secondary='eventcol_defenders',
                                backref='defender_collections',
                                primaryjoin=tjb("Event_Collection", 
                                                "eventcol_defenders",
                                                ("id", "eventcol_id")),
                                secondaryjoin=tjb("Historical_Figure", 
                                                  "eventcol_defenders",
                                                  ("id", "hfid")))

    noncoms = db.relationship('Historical_Figure', 
                                viewonly=True,
                                secondary='eventcol_noncoms',
                                backref='noncom_collections',
                                primaryjoin=tjb("Event_Collection", 
                                                "eventcol_noncoms",
                                                ("id", "eventcol_id")),
                                secondaryjoin=tjb("Historical_Figure", 
                                                  "eventcol_noncoms",
                                                  ("id", "hfid")))


