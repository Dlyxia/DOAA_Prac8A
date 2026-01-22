FROM python:3.11-slim
# Create an app directory to contain our application
RUN mkdir /app
# Copy requirements.txt from project folder into the image
COPY requirements.txt /app/requirements.txt
# Change our working directory in the image to /app folder
WORKDIR /app
# Install all the packages needed to run our web app
RUN pip install -r requirements.txt
# Add all files and sub-folders into the /app folder
COPY . /app
# Expose port 5000 for http communication
EXPOSE 5000
# Run gunicorn web server and bind it to the port
CMD gunicorn --bind 0.0.0.0:5000 app:app