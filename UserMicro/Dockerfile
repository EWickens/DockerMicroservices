# Use the Python3.7.2 image
FROM python:3.7.2-stretch

WORKDIR /app

ADD . ./

cmd ["cd", "app/"]
# Install the dependencies
RUN pip install -r requirements.txt

cmd ["python","app.py"]