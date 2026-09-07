from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from backend.core.config import settings


checkpoint_pool = ConnectionPool(
    conninfo=settings.checkpoint_database_url,
    max_size=10,
    kwargs={
        "autocommit": True,
        "prepare_threshold": 0,
    },
)


checkpointer = PostgresSaver(
    checkpoint_pool
)


def setup_checkpoint_database():
    checkpointer.setup()