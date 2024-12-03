from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.indexes import IndexMethod


ID = "2024-12-03T22:34:02:751980"
VERSION = "1.22.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="gmail_rules_engine", description=DESCRIPTION
    )

    manager.add_table(
        class_name="Email", tablename="email", schema=None, columns=None
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="email_id",
        db_column_name="email_id",
        column_class_name="UUID",
        column_class=UUID,
        params={
            "default": UUID4(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="gmail_message_id",
        db_column_name="gmail_message_id",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": True,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="from_address",
        db_column_name="from_address",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="to_address",
        db_column_name="to_address",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="date_received",
        db_column_name="date_received",
        column_class_name="Timestamptz",
        column_class=Timestamptz,
        params={
            "default": TimestamptzNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Email",
        tablename="email",
        column_name="subject",
        db_column_name="subject",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
