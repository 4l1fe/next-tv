# coding: utf-8

from api.media.media_list import get as get_media_list
""" Виртуальный метрод media/list """


def get(auth_user, session, id, **kwargs):
    return get_media_list(auth_user, session, units=id)
