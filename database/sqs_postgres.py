import psycopg2
import configuration
import datetime


def get_connection():
    try:
        connection = psycopg2.connect(
            host=configuration.DB_HOST,
            port=configuration.DB_PORT,
            dbname=configuration.DB_NAME,
            user=configuration.DB_USER,
            password=configuration.DB_PASSWORD
        )
        return connection
    except psycopg2.Error as e:
        raise Exception("Error: Unable to connect to the database.") from e


def check_table_exists(table_name):
    try:
        with get_connection() as connection, connection.cursor() as cursor:
            query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
            cursor.execute(query)
            return cursor.fetchone()[0]
    except psycopg2.Error as e:
        raise Exception("Error while checking table existence.") from e


def create_user_logins_table():
    """
    Create the 'user_logins' table in the PostgreSQL database if it does not exist.

    Raises:
        Exception: If there is an error while creating the table.
    """
    table_name = 'user_logins'
    if not check_table_exists(table_name):
        try:
            with get_connection() as connection, connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_logins(
                        user_id varchar(128),
                        device_type varchar(32),
                        masked_ip varchar(256),
                        masked_device_id varchar(256),
                        locale varchar(32),
                        app_version numeric,
                        create_date date
                    );
                """)
                connection.commit()
        except psycopg2.Error as e:
            raise Exception("Error while creating user_logins table.") from e

import logging

logging.basicConfig(level=logging.DEBUG)

def write_to_postgres(data):
    try:
        with get_connection() as connection, connection.cursor() as cursor:
            for record in data:
                logging.debug(f"Processing record: {record}")
                # Format the create_date or use the current date if it's missing or invalid
                if 'create_date' not in record or not isinstance(record['create_date'], (datetime.date, datetime.datetime)):
                    logging.warning(f"create_date missing or invalid in record {record['user_id']}; using current date.")
                    record['create_date'] = datetime.datetime.now().date().strftime('%Y-%m-%d')
                else:
                    record['create_date'] = record['create_date'].strftime('%Y-%m-%d')
                
                # Handle app_version
                try:
                    record['app_version'] = int(float(record['app_version']))  # Convert to integer after interpreting as float
                except ValueError:
                    logging.error(f"Invalid app_version format: {record['app_version']}")
                    continue  # Skip this record or handle the error as needed

                cursor.execute("""
                    INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    record['user_id'],
                    record['device_type'],
                    record['masked_ip'],
                    record['masked_device_id'],
                    record['locale'],
                    record['app_version'],
                    record['create_date']
                ))
            connection.commit()
    except Exception as e:
        logging.error(f"Error while writing to Postgres: {str(e)}")
        raise Exception(f"Error while writing to Postgres: {str(e)}") from e