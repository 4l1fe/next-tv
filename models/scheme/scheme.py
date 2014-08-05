# coding: utf-8

from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.scheme.constants import KLASS_TYPE, M_SCHEME_INT


class Scheme(Base):
    __tablename__ = 'scheme'

    id           = Column(Integer, primary_key=True)
    topic_name   = Column(String, ForeignKey('topics.name'), nullable=True)
    klass        = Column(ChoiceType(KLASS_TYPE), nullable=False, default=M_SCHEME_INT, index=True)
    name         = Column(String, nullable=False)
    type         = Column(String, nullable=False, default='')
    access_level = Column(SmallInteger, nullable=False, default=0)
    status       = Column(SmallInteger, nullable=False, default=0)
    internal     = Column(Boolean, nullable=False, default=0)

    users_value   = relationship('UsersValues', backref='scheme', cascade='all, delete')
    persons_value = relationship('PersonsValues', backref='scheme', cascade='all, delete')
    topics_value  = relationship('TopicsValues', backref='scheme', cascade='all, delete')
