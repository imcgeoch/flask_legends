from . import db
from .join_builder import join_builder as jb

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_string = db.Column(db.String(100))
    page_number = db.Column(db.Integer)
    # page_written_content_id = db.Column(db.Integer) redundant scroll vs book
    written_content_id = db.Column(db.Integer)
    holder_hfid = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    structure_local_id = db.Column(db.Integer)

    item_type = db.Column(db.String(20))
    item_subtype = db.Column(db.String(20))
    item_description = db.Column(db.String(200))
    mat = db.Column(db.String(40))
    
    events = db.relationship('Historical_Event', backref='artifact', 
                    primaryjoin='and_(Historical_Event.artifact_id == ' +
                                        'Artifact.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Artifact.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True, 
                    viewonly=True)

    def __repr__(self):
        return "<Artifact %s>" % (self.name)


class Written_Content(db.Model):
    __tablename__ = 'written_contents'
    
    forms = ['musical composition', 'choreography', 'poem', 'guide',
             'essay', 'manual', 'cultural history', 'star chart', 
             'letter', 'short story', 'cultural comparison', 'novel', 
             'autobiography', 'comparative biography', 'biography',
             'chronicle','dictionary','play','encyclopedia', 'dialog', 
             'genealogy', 'treatise on technological evolution', 'atlas',
             'alternate history', 'star catalogue', 'biographical dictionary']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    form = db.Column(db.Enum(*forms, name='wc_form_types'))
    form_id = db.Column(db.Integer) # use primaryjoin with form_id == TYPE 
    author_hfid = db.Column(db.Integer)
    author_roll = db.Column(db.Integer)

    copies = db.relationship('Artifact', backref='written_content',
            foreign_keys='Artifact.written_content_id, Artifact.df_world_id',
            primaryjoin=jb('Artifact', 'Written_Content', ('written_content_id', 'id')),
            viewonly=True) 

    styles = db.relationship('Style', 
                             foreign_keys="Style.df_world_id,"
                                          "Style.content_id",
                             primaryjoin=jb("Written_Content", 
                                            "Style",
                                            ("id", "content_id")))
    
    referenced_hfs = db.relationship('Historical_Figure',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='HISTORICAL FIGURE')"  ,
            secondaryjoin=jb("Historical_Figure", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_events = db.relationship('Historical_Event',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='HISTORICAL EVENT')"  ,
            secondaryjoin=jb("Historical_Event", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_sites = db.relationship('Site',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='SITE')"  ,
            secondaryjoin=jb("Site", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_sites = db.relationship('Artifact',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='ARTIFACT')"  ,
            secondaryjoin=jb("Artifact", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_regions = db.relationship('Entity',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='ENTITY')"  ,
            secondaryjoin=jb("Entity", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_sites = db.relationship('Region',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='SUBREGION')"  ,
            secondaryjoin=jb("Region", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_wcs = db.relationship('Written_Content',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='WRITTEN CONTENT')"  ,
            secondaryjoin=jb("Written_Content", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_poetic_forms = db.relationship('Poetic_Form',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='POETIC FORM')"  ,
            secondaryjoin=jb("Poetic_Form", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_dance_forms = db.relationship('Dance_Form',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='DANCE FORM')"  ,
            secondaryjoin=jb("Dance_Form", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)
    referenced_musical_forms = db.relationship('Musical_Form',
            secondary="references",
            primaryjoin="and_( (" + jb("Written_Content", "Reference", ("id", "wc_id"))
                        + "), Reference.type=='MUSICAL FORM')"  ,
            secondaryjoin=jb("Musical_Form", "Reference", ("id", "ref_id")),
            foreign_keys="Reference.wc_id, Reference.ref_id",
            backref="referencing_works",
            viewonly=True)

    def style_string(self):
        styles = self.styles[:]
        if styles == []:
            return ""
        last_style = styles.pop().as_string()
        style_list = ", ".join([style.as_string() for style in styles]) + " and " if styles else ""
        return style_list + last_style



class Reference(db.Model):
    __tablename__ = 'references'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', 
        ondelete='CASCADE'))
    type = db.Column(db.String(30))
    ref_id = db.Column(db.Integer)
    wc_id = db.Column(db.Integer)

class Style(db.Model):
    __tablename__ = 'styles'

    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    content_id = db.Column(db.Integer)
    style = db.Column(db.String(20)) #should be enum
    magnitude = db.Column(db.Integer)

    def as_string(self):
        if self.magnitude == 1:
            return "a little " + self.style
        elif self.magnitude == 2:
            return "somewhat " + self.style
        elif self.magnitude == 3:
            return "quite " + self.style
        elif self.magnitude == 4:
            return "very " + self.style
        else:
            return self.style

class Musical_Form(db.Model):
    __tablename__ = 'musical_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    name = db.Column(db.String(50))

class Poetic_Form(db.Model):
    __tablename__ = 'poetic_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    name = db.Column(db.String(50))

class Dance_Form(db.Model):
    __tablename__ = 'dance_forms'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    name = db.Column(db.String(50))

class Historical_Era(db.Model):
    __tablename__ = 'historical_eras'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    start_year = db.Column(db.Integer)

    def __repr__(self):
        return "<Historical Era %s>" % (self.name)

