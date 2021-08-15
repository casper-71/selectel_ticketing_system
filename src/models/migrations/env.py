from logging.config import dictConfig

from src.core.config.database_settings import DBSettings
from src.core.logger import LOGGING
from src.db.postgresql import Base
from src.models import tickets, comments        # noqa: F401

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config     # pylint: disable=no-member
app_db_settings = DBSettings()

# Database settings
section = config.config_ini_section
config.set_section_option(section, "DB_DSN", f'{app_db_settings.pg_dsn}')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
dictConfig(LOGGING)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(                      # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():       # pylint: disable=no-member
        context.run_migrations()            # pylint: disable=no-member


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(                  # pylint: disable=no-member
            connection=connection, target_metadata=target_metadata          # pylint: disable=no-member
        )

        with context.begin_transaction():       # pylint: disable=no-member
            context.run_migrations()            # pylint: disable=no-member


if context.is_offline_mode():                   # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()
