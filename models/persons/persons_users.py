# coding: utf-8

import time

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from models import Base


class UsersPersons(Base):
    __tablename__ = 'users_persons'
    __table_args__ = (
        UniqueConstraint('user_id', 'person_id', name='_user_id_person_id'),
    )

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    person_id  = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    subscribed = Column(DateTime)
    liked      = Column(DateTime)


    @classmethod
    def tmpl_for_user_person(cls, session):
        query = session.query(cls)
        return query


    @classmethod
    def get_user_person(cls, user_id, person_id, session):
        query = cls.tmpl_for_user_person(session).filter(cls.user_id == user_id, cls.person_id == person_id)
        return query


    @classmethod
    def cls_check_liked(cls, value):
        return time.mktime(value.timetuple()) if not value is None else 0


    @classmethod
    def cls_check_subscribed(cls, value):
        return True if not value is None else False


    @property
    def check_liked(self):
        return time.mktime(self.liked.timetuple()) if not self.liked is None else 0


    @property
    def check_subscribed(self):
        return True if not self.subscribed is None else False


    def __repr__(self):
        return u"<UsersPersons(user={0}, person={1}, subscr={2}, liked={3})>".\
            format(self.user_id, self.person_id, self.subscribed, self.liked)


def validate_subcribe(mapper, connect, target):
    if target.user_id == target.person_id:
        raise ValueError(u'Нельзя подписаться на самого себя')

listen(UsersPersons, 'before_insert', validate_subcribe)