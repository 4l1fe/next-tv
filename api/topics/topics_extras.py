# coding: utf-8

from models import db, Topics, ExtrasTopics
from models.extras.constants import EXTRA_TYPE

from utils.validation import validate_mLimit

__all__ = ['get_topic_extars']


@db
def get_topic_extars(user, session, **kwargs):
    # Params
    params = {
        'id': None,
        'text': None,
        'type': None,
        'limit': None,
    }

    if 'id' in kwargs:
        id = kwargs['id']
        if not isinstance(id, list):
            try:
                params['id'] = [int(kwargs['id'])]
            except Exception, e:
                pass
        else:
            if isinstance(id, list):
                try:
                    params['id'] = [int(i) for i in id]
                except Exception, e:
                    pass

    if 'text' in kwargs:
        try:
            params['text'] = str(kwargs['text']).strip()
        except:
            pass

    if 'type' in kwargs:
        if kwargs['type'] in dict(EXTRA_TYPE).keys():
            params['type'] = kwargs['type']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(limit=kwargs['limit'])



    return {}
