#coding: utf-8
import argparse

import settings
from models import Base
from utils.connection import db_connect, create_session


parser = argparse.ArgumentParser(description=u'Synchronize tables for NextTV service')
parser.add_argument('-d', '--database', dest='database', action='store_true', default='postgresql',
                    help=u'Run server with test params')
parser.add_argument('-c', '--create', dest='create', action='store_true', default=False,
                    help=u'Create database for project')

args = parser.parse_args()


if not args.database in settings.DATABASE.keys():
    raise Exception(u'Необходим ключ базы данных из конфига')


if args.create:
    original_dbname = settings.DATABASE[args.database]['database']
    settings.DATABASE[args.database]['database'] = 'template1'

    session = create_session(bind=db_connect(type=args.database))
    session.connection().connection.set_isolation_level(0)

    sql = """
        CREATE DATABASE {0} WITH OWNER={1} ENCODING='UTF8'
        TABLESPACE=pg_default LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' CONNECTION LIMIT=-1;
    """

    print u"Creating database: {0}".format(original_dbname)
    session.execute(sql.format(original_dbname, settings.DATABASE[args.database]['username']))

    session.connection().connection.set_isolation_level(1)
    settings.DATABASE[args.database]['database'] = original_dbname


print u'Creating tables'
Base.metadata.create_all(bind=db_connect(type=args.database))

# TODO: Здесь должен быть код для запуска миграций alembic

print u'Finished setting up database'
