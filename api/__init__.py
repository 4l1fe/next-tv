# coding: utf-8

from models import Users, db
from users import routing as users_routing
from topics import routing as topics_routing
from persons import routing as persons_routing
from test import routes as test_routing
from user import  routing as user_routing


routes = {
    'user': user_routing,
    'users': users_routing,
    'topics': topics_routing,
    'persons': persons_routing,
    'test': test_routing
}

@db
def authorize(token, session=None):
    if token == 'foobar':
        return session.query(Users).filter_by(id=1).first()
    elif token == 'snafu':
        return session.query(Users).filter_by(id=2).first()
    else:
        return None

