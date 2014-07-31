# coding: utf-8

import zerorpc
import unittest
import datetime

from tests.constants import ZERORPC_SERVICE_URI
from tests.create_test_user import create
from tests.fixtures import create_topic, create_user_topic, create_cdn, create_extras, create_topic_extras

from models import Base, SessionToken, UsersTopics, Users
from utils.connection import db_connect, create_session


def setUpModule():
    engine = db_connect().connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_user_topic(session)
    create_cdn(session)
    create_extras(session)
    create_topic_extras(session)

    engine.close()


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


###################################################################################
class TopicInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)


        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "info",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {
            'name': 'test',
            'title': 'test',
            'title_orig': None,
            'description': 'test test',
            'releasedate': 1388534400.0,
            'type': 'news',
            'relation': {
                'subscribed': False,
                'liked': 0,
            }
        }

        self.assertDictEqual(temp, resp)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo_get(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {'liked': 0}

        self.assertDictEqual(temp, resp)


    def test_echo_post(self):
        topic = "test1"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.liked, None)


    def test_echo_delete(self):
        topic = "test2"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.liked, None)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicSubscribeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo_get(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {'subscribed': 0}

        self.assertDictEqual(temp, resp)


    def test_echo_post(self):
        topic = "test2"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.subscribed, None)


    def test_echo_delete(self):
        topic = "test1"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.subscribed, None)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicExtrasTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect(ZERORPC_SERVICE_URI)


    def test_echo(self):
        topic = 'test'
        IPC_pack = {
            "api_group": "topics",
            "api_method": "extras",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)

        temp = [
            {
                'description': 'test test',
                'created': 1388534400.0,
                'title': 'test',
                'title_orig': 'test',
                'location': 'russia',
                'type': 'v',
                'id': 1
            }, {
                'description': 'test1 test',
                'created': 1388534400.0,
                'title': 'test1',
                'title_orig': 'test1',
                'location': 'russia',
                'type': 'v',
                'id': 2
            }
        ]

        self.assertListEqual(temp, resp)

    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicListTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)


    def test_echo(self):
        topic = 'news'
        IPC_pack = {
            "api_group": "topics",
            "api_method": "list",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                "type": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(len(resp), 2)

        temp = [
            {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400.0,
                'relation': {},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            }, {
                'description': 'test test',
                'title': 'test',
                'releasedate': 1388534400.0,
                'relation': {},
                'title_orig': None,
                'type': 'news',
                'name': 'test'
            }
        ]
        self.assertListEqual(temp, resp)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicValuesTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)

    def test_echo(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "values",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                "name": topic,
                "scheme_name": "t",
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = []

        self.assertEqual(temp, resp)

    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicMediaTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)


    def test_echo(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "media",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = []

        self.assertEqual(temp, resp)

    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicPersonsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect(ZERORPC_SERVICE_URI)


    def test_echo(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "persons",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = []

        self.assertEqual(temp, resp)

    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()
