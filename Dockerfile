# Use an official Python runtime as a parent image
FROM python:3.8

# Install system dependencies for WeasyPrint, OpenCV, and TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    libpango1.0-0 \
    libcairo2 \
    libpangocairo-1.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    libgl1-mesa-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install TensorFlow
RUN pip install tensorflow

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "./app.py"]
