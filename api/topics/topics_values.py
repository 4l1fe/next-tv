# coding: utf-8

from models import dbWrap, TopicsValues
from models.scheme import Scheme

__all__ = ['get_topic_values']


@dbWrap
def get_topic_values(user, session, name, **kwargs):
    # Params
    params = {
        'name': name,
        'session': session,
        'scheme_name': None,
    }

    if 'scheme_name' in kwargs:
        scheme_name = kwargs['scheme_name']
        if not isinstance(scheme_name, list):
            try:
                params['scheme_name'] = [str(scheme_name).strip()]
            except Exception, e:
                pass
        else:
            if isinstance(scheme_name, list):
                try:
                    params['scheme_name'] = [str(i).strip() for i in scheme_name]
                except Exception, e:
                    pass

    if params['scheme_name'] is None:
        #return 404
        pass

    query = TopicsValues.get_values_through_schema(**params).all()

    return TopicsValues.data(query)
