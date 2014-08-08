# coding:utf-8

from models.users import Users
from models.tokens import SessionToken
from models.persons import Persons
from models.chats import UsersChat
from models.mongo import ChatMessages
from utils.validation import validate_int
from api.serializers import mPersonSerializer as mP


def get_chat_stat(id, auth_user, session, **kwargs):
    chat = validate_int(id)

    users = session.query(Users).join(UsersChat).filter(UsersChat.chat_id==chat)
    on_users = SessionToken.filter_users_is_online(True, users)
    on_users_count = on_users.count()  # тип - long
    persons = session.query(Persons).join(Users).filter(Persons.user_id.in_([u.id for u in on_users.all()])).all()
    mp = mP(instance=persons, user=auth_user, session=session)
    p_data = mp.data
    data = {'user_cnt': int(on_users_count), 'persons': p_data}
    if auth_user:
        uc = session.query(UsersChat).filter_by(user_id=auth_user.id).one()
        last_update = uc.last_update
        new_msgs_count = ChatMessages.objects.filter(chat_id=chat, created__gt=last_update).count()
        data.update({'new_msgs': new_msgs_count})

    return data
