# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /flask_app

# Copy the current directory contents into the container at /flask_app
COPY . /flask_app

RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir pyvis
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir SQLAlchemy


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
