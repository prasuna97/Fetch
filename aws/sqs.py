import json
import boto3
import os
from botocore.config import Config

# Set AWS environment variables for local testing
os.environ["AWS_ACCESS_KEY_ID"] = "dummy_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "dummy_secret_key"

def read_data_from_sqs(queue_name):
    try:
        # Create an SQS client with custom endpoint and region
        config = Config(retries={'max_attempts': 10, 'mode': 'standard'})
        sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1', config=config)
        
        # Receive messages from the specified SQS queue
        response = sqs.receive_message(
            QueueUrl=f'http://localhost:4566/000000000000/{queue_name}',
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )

        # Extract messages from the response
        messages = response.get('Messages', [])

        # Parse and store the JSON data from each message
        data = []
        for message in messages:
            data.append(json.loads(message['Body']))

            # Delete the processed message from the SQS queue
            sqs.delete_message(QueueUrl=f'http://localhost:4566/000000000000/{queue_name}', ReceiptHandle=message['ReceiptHandle'])

        return data

    except Exception as e:
        raise Exception(f"Error while reading from SQS: {str(e)}") from e