import datetime

from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.schema import Table, Column, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Integer, Boolean, DateTime, JSON

from ..extensions import db


Base = db.Model

class Design(Base):
    id         = Column(Integer, primary_key = True)
    name       = Column(String(100), nullable=False)


class Creation(Base):
    __tablename__ = 'creation'

    id         = Column(Integer, primary_key = True)
    name       = Column(String(100), nullable=False)
    domain     = Column(String(100), nullable=False, unique=True)
    active     = Column(Boolean, nullable=False)
    id_design  = Column(Integer, ForeignKey(Design.id), nullable=False)

    menu       = Column(JSON)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    design     = relationship(Design, backref='page', lazy=False)

    @hybrid_property
    def pages(self):
        return Page.query.filter_by(creation=self)


class Page(Base):
    __tablename__ = 'page'

    id          = Column(Integer, primary_key = True)
    id_creation = Column(Integer, ForeignKey(Creation.id), nullable=False)
    name        = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    creation    = relationship(Creation, backref='page', lazy=True)

    @hybrid_property
    def components(self):
        return Component.query.filter_by(page=self)


class Component(Base):
    __tablename__ = 'component'

    id         = Column(Integer, primary_key = True)
    name       = Column(String(100), nullable=False)
    type       = Column(String(100), nullable=False)
    sort       = Column(Integer)
    config     = Column(JSON)
    id_page    = Column(Integer, ForeignKey(Page.id), nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    page       = relationship(Page, backref='component', lazy=True)

