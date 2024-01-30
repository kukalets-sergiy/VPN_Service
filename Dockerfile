# Use the Python 3.10.8 base image
FROM python:3.10.8
# Prevent Python from writing pyc files to disk (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure that Python output is sent straight to terminal without buffering it first
ENV PYTHONUNBUFFERED=1
# Set the working directory inside the container to /code
WORKDIR /code
# Copy the requirements.txt file from the current local directory to the /code directory in the container
COPY requirements.txt /code/
# Install the Python dependencies specified in requirements.txt using pip
RUN pip install -r requirements.txt
# Copies all files and folders from the current local directory to the /code/ working directory inside the container.
COPY . /code/



