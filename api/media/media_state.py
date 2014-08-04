# coding: utf-8
import datetime
from models.media.media import Media
from models.media.users_media import UsersMedia
from utils.date_converter import detetime_to_unixtime as convert_date
from utils.validation import validate_int


def get(id, auth_user, session, **kwargs):
    data = {
        'watched': 0,
        'pos': None
    }

    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if users_media:
        watched = convert_date(users_media.watched) if users_media.watched else 0
        data.update(watched=watched)
        if users_media.play_pos:
            data.update(pos=users_media.play_pos)
        return data
    return data


def post(id, auth_user, session, watched=None, pos=None, **kwargs):
    date = datetime.datetime.utcnow()
    params = {
        'user_id': auth_user.id,
        'media_id': id,
    }
    if watched:
        params.update(watched=date)
    if pos:
        pos = validate_int(pos, min_value=0)
        params.update(play_pos=pos)

    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if users_media is None:
        users_media = UsersMedia(**params)
        session.add(users_media)
    else:
        if watched:
            users_media.watched = date
        if pos:
            users_media.play_pos = pos
    if session.new or session.dirty:
        session.commit()


def delete(id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if not users_media is None:
        users_media.watched = None
        users_media.play_pos = None
    if session.dirty:
        session.commit()
