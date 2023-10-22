# Use an official Python runtime as the base image
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the Django project source code into the container
COPY . /app/

# Expose the port the application will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

