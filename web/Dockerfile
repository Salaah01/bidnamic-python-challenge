FROM python:3.10.2-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install the requirements
COPY requirements* .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.dev.txt

# Copy the app files
COPY . .
