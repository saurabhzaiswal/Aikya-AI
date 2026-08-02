"""Display the effective database target without exposing its password."""

import argparse

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run a non-destructive SELECT 1.")
    parser.add_argument(
        "--tables",
        action="store_true",
        help="List public table names after a successful connection check.",
    )
    arguments = parser.parse_args()

    database_url = make_url(get_settings().DATABASE_URL)
    print("Database configuration:")
    print(f"  Dialect: {database_url.drivername}")
    print(f"  Host: {database_url.host or 'localhost'}")
    print(f"  Port: {database_url.port or 5432}")
    print(f"  Database: {database_url.database or ''}")
    print(f"  Username: {database_url.username or ''}")
    print("  Password: ********")

    if not arguments.check and not arguments.tables:
        return 0

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Connection: OK")
            if arguments.tables:
                table_names = inspect(connection).get_table_names(schema="public")
                print("Tables:")
                for table_name in table_names:
                    print(f"  - {table_name}")
    except SQLAlchemyError as error:
        print(f"Connection: FAILED ({type(error).__name__})")
        original_error = getattr(error, "orig", None)
        safe_message = str(original_error).lower() if original_error is not None else ""
        if "does not exist" in safe_message and "database" in safe_message:
            print("Reason: the configured database does not exist.")
            print('Create it manually: psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE \\"aikya-ai\\";"')
        elif "password authentication failed" in safe_message:
            print("Reason: PostgreSQL rejected the configured username/password.")
        elif "connection refused" in safe_message:
            print("Reason: no PostgreSQL server accepted the localhost connection.")
        else:
            print("Reason: PostgreSQL could not complete the connection; no credentials were printed.")
        return 1
    finally:
        engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
