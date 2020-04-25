
FROM ubuntu:18.04
FROM python:3.7.3-stretch

WORKDIR /app

COPY . app.py /app/

RUN export GOOGLE_APPLICATION_CREDENTIALS="/app/cred.json"

RUN pip install -r requirements.txt 

# Expose port 80
EXPOSE 80

# Run app.py at container launch
CMD ["python", "app.py"]


