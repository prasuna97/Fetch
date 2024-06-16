# Fetch Rewards Data Engineering Take Home

## Overview

This application is designed to process JSON data containing user login behavior from a mock AWS SQS Queue using a localstack setup. It masks personal identifiable information (PII) for privacy reasons and writes the transformed data to a PostgreSQL database. This system is set up to run locally using Docker.

## Features

- **Data Ingestion**: Reads JSON messages from an emulated AWS SQS queue.
- **Data Transformation**: Masks PII fields (`device_id`, `ip`) in a reversible way for data analysts to easily identify duplicates.
- **Data Storage**: Writes processed data to a pre-configured PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- Access to a terminal or command line interface
- awscli-local (install via pip install awscli-local)
- PostgreSQL (installed via Docker)

## How to run this project
1. clone this repo to the local machine
2. Install Docker & Docker compose
3. Initialize the docker containers for local stack and postgresql by using the commonad in the project directory (docker-compose up -d)
4. Containers should be up and running after the above step
5. Now we can run the main.py
6. Later in your system search for psql command prompt to query,here you need to provide postgres credentials , then you can test if the data has been loaded

## Application Structure

- `aws/`: Contains AWS related scripts including the SQS message reader (`sqs.py`).
- `database/`: Contains scripts interacting with PostgreSQL (`sqs_postgres.py`).
- `pii/`: Includes the PII masking logic (`masking.py`) and configuration files.
- `venv/`: Python virtual environment for managing dependencies.
- `Dockerfile`: Defines the Docker container that runs the application.
- `docker-compose.yml`: Composes the Docker services including localstack and PostgreSQL.
- `main.py`: The main entry point of the application.
- `requirements.txt`: Lists all Python libraries the project depends on.
- `README.md`: Provides project documentation.

## Launch the application along with localstack and PostgreSQL containers 
```bash
docker-compose up -d
```
## Run the Python Script
```bash
python main.py
```
## Testing 
To retrieve a message from the queue, utilize the awslocal tool:
  ```
  awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
  ```
To establish a connection with the PostgreSQL database and confirm the table's existence, execute the following command:
  ```
  psql -d postgres -U postgres -p 5432 -h localhost -W
  ```
Afterward, run the subsequent SQL command:
```
  SELECT * FROM user_logins;
  ```

## Future enhancements

### Deployment in Production
Deploy the application using AWS ECS or Kubernetes for container orchestration, ensuring scalability and reliability. Replace Localstack with actual AWS services and configure secure environment variables and credentials using AWS Secrets Manager.

### Components for Production Readiness
Add components such as a load balancer for traffic distribution, automated backup solutions for data persistence, and integrate a CI/CD pipeline for automated testing and deployment. Implement comprehensive logging and monitoring using tools like ELK Stack or Amazon CloudWatch.

### Scaling Strategy
Scale the application by implementing database scaling options such as read replicas. Utilize Kubernetes for dynamic horizontal scaling based on load, and introduce caching mechanisms like Redis to manage database load efficiently.

### PII Recovery Strategy
Implement reversible masking techniques for PII that allow for secure decoding by authorized personnel only. Store the keys for reversing the masking in a secure service like AWS KMS, with strict access controls and regular key rotation.

### Assumptions
Assumptions includes consistent data formats from AWS SQS, stable and similar conditions between the development and production environments, and uninterrupted availability of AWS services and Docker images. Compliance with all relevant security regulations for PII handling is assumed.