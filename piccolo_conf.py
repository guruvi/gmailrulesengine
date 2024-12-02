"""The configurations for piccolo."""


from piccolo.conf.apps import AppRegistry
from piccolo.engine import SQLiteEngine

DB = SQLiteEngine(path='gmailrulesengine.sqlite')

APP_REGISTRY = AppRegistry(apps=["gmail_rules_engine.piccolo_app"])
