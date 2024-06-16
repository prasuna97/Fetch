# Set the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install required dependencies
RUN pip install -r "requirements.txt"

# Command to run the application
CMD ["python", "main.py"]