FROM ubuntu:latest
MAINTAINER Jim Hendricksa "jhendric98@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential sqlite
COPY . /python_rest
WORKDIR /python_rest
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]
