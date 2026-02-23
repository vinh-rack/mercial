import psycopg

from shared.config import settings


def get_db_connection():
    return psycopg.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        dbname=settings.db
    )
