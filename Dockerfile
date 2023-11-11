# Use an official Python runtime as a parent image
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Update pip
RUN pip install --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Command to run the application
ENTRYPOINT ["python", "run.py"]
