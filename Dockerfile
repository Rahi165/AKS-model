# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure stdout/stderr is displayed in real time

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the working directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the collectstatic command for static files (if applicable)
#RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Command to start the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]