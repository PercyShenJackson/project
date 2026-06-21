# Use the latest official Python 3.14 slim image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your local application files
COPY . .

# Specify the command to run your script
CMD ["python", "app.py"]
