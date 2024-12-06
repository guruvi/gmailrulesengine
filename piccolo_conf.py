"""The configurations for piccolo."""


import os
from piccolo.conf.apps import AppRegistry
from piccolo.engine import SQLiteEngine

sqlite_engine = os.getenv('DATABASE_NAME')
DB = SQLiteEngine(path=sqlite_engine)

APP_REGISTRY = AppRegistry(apps=["gmail_rules_engine.piccolo_app"])
