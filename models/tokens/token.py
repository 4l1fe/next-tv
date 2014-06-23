#coding: utf-8
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from models import Base

import datetime
import os
import base64


def token_gen(token_length):
    def get_token():
        return base64.b64encode(os.urandom(token_length), '00')
    return get_token


class TokenMixin(Base):
    __abstract__ = True

    token_length = 48

    @declared_attr
    def id(cls):
        return Column(Integer,nullable=False, primary_key= True, index =True)

    @declared_attr
    def user_id(cls):
        return Column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    @declared_attr
    def token(cls):
        return Column('token', String(64), default=token_gen(cls.token_length))

    @declared_attr
    def created(cls):
        return Column('created', DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return u'<{}({}-{})>'.format(self.__class__.__name__, self.user_id, self.token)

    @classmethod
    def get_tmpl(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def generate_token(cls, user_id, session=None):
        '''
        (Re)Generate token for given user_id
        '''
        qr = session.query(cls).filter(cls.user_id == user_id).first()

        if qr is None:
            gt = cls(user_id=user_id)
            session.add(gt)
            session.commit()
            return gt.token

        else:
            gt, = qr
            gt.token = cls.token_gen(cls.token_length)
            session.add(gt)
            session.commit()
            return gt.token