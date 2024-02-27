# Choose base image
FROM python:3.11

# Create dir
WORKDIR /schedule-shows-productions

# Install dependencies
COPY ./requirements.txt /schedule-shows-productions/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /schedule-shows-productions/requirements.txt

# Copy necessary files
COPY . /schedule-shows-productions/


# Run tests first, then start server
CMD ["/bin/bash","-c","pytest -v; uvicorn main:app --reload --host 0.0.0.0 --port 80"]