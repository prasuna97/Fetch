import logging
from aws import sqs
from database import sqs_postgres
from pii import masking
import configuration

table_name = 'user_logins'

def setup_logging():
    """
    Set up logging configuration to log messages with date and time, and level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    try:
        setup_logging()

        # Step 1: Set Up Docker Environment (Run LocalStack and Postgres containers)
        # No code for Step 1 in this script. Assumes that Docker environment is already set up.

        # Step 2: Read Data from AWS SQS Queue
        logging.info("Reading data from AWS SQS Queue...")
        sqs_queue_name = configuration.SQS_QUEUE_NAME
        data = sqs.read_data_from_sqs(sqs_queue_name)

        # Step 3: Transform the Data
        logging.info("Transforming the data...")
        transformed_data = masking.mask_pii_data(data)

        # Step 4: Check if the 'user_logins' table exists in Postgres Database
        if not sqs_postgres.check_table_exists(table_name):
            # If the table does not exist, create it.
            logging.info("Creating 'user_logins' table in Postgres Database...")
            sqs_postgres.create_user_logins_table()

        # Step 5: Write to Postgres Database
        logging.info("Writing data to Postgres Database...")
        sqs_postgres.write_to_postgres(transformed_data)

        logging.info("Data processing and writing to Postgres completed successfully!")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        # You may choose to log the error or send an alert/notification here.

if __name__ == "__main__":
    main()