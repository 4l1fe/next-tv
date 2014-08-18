# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime,\
    and_, SMALLINT
from sqlalchemy.orm import relationship, contains_eager
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.media.constants import APP_MEDIA_LIST
from models.media.users_media_units import UsersMediaUnits


class MediaUnits(Base):
    __tablename__ = 'media_units'

    id            = Column(Integer, primary_key=True)
    topic_name    = Column(String, ForeignKey('topics.name'), nullable=False)
    title         = Column(String, nullable=False)
    title_orig    = Column(String, nullable=True)
    description   = Column(Text, nullable=True)
    previous_unit = Column(Integer, nullable=True)
    next_unit     = Column(Integer, nullable=True)
    release_date  = Column(DateTime, nullable=True)
    end_date      = Column(DateTime, nullable=True)
    batch         = Column(String, nullable=True)
    access        = Column(SMALLINT, default=None, nullable=True)
    access_type   = Column(ChoiceType(APP_MEDIA_LIST), default=None, nullable=True)

    countries_list   = relationship('MediaUnitsAccessCountries', backref='media_units', cascade='all, delete')
    user_media_units = relationship('UsersMediaUnits', backref='media_units', cascade='all, delete')
    unit_medias      = relationship('MediaInUnit', backref='media_units', cascade='all, delete')


    @classmethod
    def tmpl_for_media_units(cls, user, session):
        query = session.query(cls)

        if not user is None:
            query = query.\
                outerjoin(UsersMediaUnits, and_(cls.id == UsersMediaUnits.media_unit_id, UsersMediaUnits.user_id == user.id)).\
                options(contains_eager(cls.user_media_units))

        return query

    @classmethod
    def get_media_units_list(cls, user, session, id=None, text=None, batch=None, topic=None):
        query = cls.tmpl_for_media_units(user, session)

        if not id is None:
            query = query.filter(cls.id.in_(id))

        if not text is None:
            query = query.filter(cls.title == text)

        if not batch is None:
            query = query.filter(cls.batch == batch)

        if not topic is None:
            query = query.filter(cls.topic_name == topic)

        return query

    @classmethod
    def get_media_unit_by_id(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).filter(cls.id == id).first()
        return query

    @classmethod
    def get_prev_media_unit(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).filter(cls.id == session.query(cls.previous_unit).filter(cls.id == id).subquery()).first()
        return query

    @classmethod
    def get_next_media_unit(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).filter(cls.id == session.query(cls.next_unit).filter(cls.id == id).subquery()).first()
        return query

    def __repr__(self):
        return u'<MediaUnits(id={0}, title={1})>'.format(self.id, self.title)
