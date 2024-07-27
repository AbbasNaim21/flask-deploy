# Use the official Python image from the Docker Hub
FROM python:3.12.3

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Set the working directory in the container
RUN set -ex && mkdir /translator
WORKDIR /translator

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy the relevant directories
COPY model/ ./model
COPY . ./

# Expose the port Flask will run on
EXPOSE 8000

# Command to run the Flask application
CMD python /translator/app.py
