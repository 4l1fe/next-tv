# coding: utf-8

import time
import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, and_
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from models.extras.constants import EXTRA_TYPE

from models import Base
from models.extras.extras_topics import ExtrasTopics


class Extras(Base):
    __tablename__ = 'extras'


    id          = Column(Integer, primary_key=True)
    cdn_name    = Column(String, ForeignKey('cdn.name'), nullable=False)
    type        = Column(ChoiceType(EXTRA_TYPE), nullable=False)
    location    = Column(String, nullable=False)
    created     = Column(DateTime, default=datetime.datetime.now)
    description = Column(Text, nullable=False)
    title       = Column(String, nullable=False)
    title_orig  = Column(String, nullable=False)


    @classmethod
    def tmpl_for_extras(cls, session):
        return session.query(cls)


    @classmethod
    def get_extras_by_topics(cls, session, name, id=None, text=None, _type=None, limit=None):
        query = cls.tmpl_for_extras(session).join(ExtrasTopics, and_(cls.id == ExtrasTopics.extras_id, ExtrasTopics.topic_name == name))

        # Set name filter
        if not id is None:
            query = query.filter(cls.id.in_(id))

        # Set description filter
        if not text is None:
        #     query = query.filter(cls.description == text)
            pass

        # Set type filter
        if not _type is None:
            query = query.filter(cls.type == _type)

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if not limit[0] is None:
                query = query.offset(limit[1])

        return query


    @classmethod
    def data(cls, data):
        if isinstance(data, list):
            data = [item.to_native() for item in data]
        else:
            data = data.to_native()

        return data


    def to_native(self):
        result = {
            'id': self.id,
            'type': self.get_type_code,
            'title': self.title,
            'title_orig': self.title_orig,
            'description': self.description,
            'location': self.location,
            'created': self.get_unixtime,
        }

        return result


    @property
    def get_type_code(self):
        return self.type.code


    @property
    def get_unixtime(self):
        return time.mktime(self.created.timetuple())