# Use an official Python runtime as a parent image
FROM python:3.6-slim
#FROM ubuntu

# Update the image to the latest packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y iputils-ping

# Identify the maintainer of an image
LABEL maintainer="mike.bison42@googlemail.com"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV HOST wikipedia.de

# Run app.py when the container launches
CMD ["python", "app.py"]
