import asyncio
import pathlib
import sys
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from alembic import context

# Allow alembic to import from your app directory
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.core.config import Settings
# This imports all your SQLModel classes from your models directory,
# populating the SQLModel.metadata object.
from app.models import *

# ------------------- Configuration -------------------

# Alembic Config object, which provides access to the .ini file
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get your database URL from your application settings
settings = Settings()
db_url = str(settings.ASYNC_DATABASE_URI)

# Your models' metadata object for 'autogenerate' support
target_metadata = SQLModel.metadata

# A set of all table names defined in your models.
# This is the key for the safety hook below.
my_model_tables = set(target_metadata.tables.keys())


def include_object(object, name, type_, reflected, compare_to):
    """
    The safety hook. This function tells Alembic to only "see" the tables
    that are explicitly defined in your SQLModel classes. It will ignore
    all other tables in the shared database during autogeneration.
    """
    if type_ == "table":
        return name in my_model_tables
    # For other objects like indexes, you can decide how to handle them
    return True

# ------------------- Migration Functions -------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Add the safety hook for completeness
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """The synchronous function that Alembic will run."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Add the safety hook here. This is the most critical part.
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """The async wrapper to run migrations in 'online' mode."""
    connectable = create_async_engine(db_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ------------------- Execution -------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())