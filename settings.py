# coding: utf-8
import os
import yaml

DEBUG = True

BASE_PATH = os.path.dirname(__file__)

CONFIG_PATH = os.path.join(BASE_PATH, 'configs')

DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.BaseLoader)

TOKEN_LIFETIME = 15