from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.schema import MetaData

config = context.config
target_metadata = MetaData(schema="test")


def run_migrations_online():
    connectable = config.attributes.get('connection', None)

    if connectable is None:
        cmd_line_url = context.get_x_argument(as_dictionary=True).get('url')
        if cmd_line_url:
            connectable = create_engine(cmd_line_url)
        else:
            raise Exception("No connection URL. Use '-x url=<url>'")

        @event.listens_for(connectable, "connect")
        def set_schema(dbapi_connection, connection_record):
            with dbapi_connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO test,public')

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="test"
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
