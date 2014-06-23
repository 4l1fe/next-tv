#coding: utf-8
from sqlalchemy import Column, Boolean
from sqlalchemy.sql.expression import or_

from token import TokenMixin
from settings import TOKEN_LIFETIME

import datetime


class SessionToken(TokenMixin):
    __tablename__ = "session_tokens"

    is_active = Column(Boolean, default=True)

    @classmethod
    def get_user_id_by_token(cls, token_string, session=None):

        st = session.query(SessionToken).filter(cls.token == token_string).first()

        if st is None:
            return None
        else:
            if (datetime.datetime.utcnow() - st.created < datetime.timedelta(minutes=TOKEN_LIFETIME)) and st.is_active:
                return st.user_id
            else:
                st.is_active = False
                session.add(st)
                session.commit()
                return None

    @classmethod
    def user_is_online(cls, user_id, session=None):
        sess = session.query(cls).filter_by(user_id=user_id).order_by(cls.created.desc()).first()
        return sess and sess.is_active and (datetime.datetime.utcnow() - sess.created < datetime.timedelta(minutes=TOKEN_LIFETIME))

    @classmethod
    def filter_users_is_online(cls, is_online, query):
        if is_online:
            query = query.join(cls).filter(cls.is_active, cls.created - datetime.datetime.utcnow() < datetime.timedelta(minutes=TOKEN_LIFETIME))
        else:
            query = query.join(cls).filter(or_(cls.is_active == False, cls.created - datetime.datetime.utcnow() >= datetime.timedelta(minutes=TOKEN_LIFETIME)))

        return query



    @classmethod
    def generate_token(cls,user_id,session):

        '''
        (Re)Generate token for given user_id
        '''

        st = SessionToken(user_id=user_id,is_active=True)
        
        session.add(st)
        session.commit()
        return st.id,st.token,st.created