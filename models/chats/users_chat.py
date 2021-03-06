# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.schema import UniqueConstraint

from models import Base


class UsersChat(Base):
    __tablename__ = 'users_chat '
    __table_args__ = {'extend_existing': True}

    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    last_update = Column(Integer)
    cuStatus = Column(String(128))

    def __init__(self, chat, user, last_update=None, cuStatus=None):
        self.chat_id = chat
        self.user_id = user
        self.last_update = last_update
        self.cuStatus = cuStatus

    def __repr__(self):
        return "<ChatUser({} {})>".format(self.chat_id, self.user_id)


