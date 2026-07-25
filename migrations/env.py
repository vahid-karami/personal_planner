import asyncio
import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
# Ensure project root is in sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# Import settings and models
from app.core.config import settings
from app.core.database import Base
import app.models  # IMPORTANT: Registers Project, Task, Note with Base.metadata

config = context.config

# Inject DB URL dynamically from settings
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata