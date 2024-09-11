# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and other necessary project files
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (if there are more files, adjust accordingly)
COPY . .

# Command to run your application
CMD ["python", "app.py"]
