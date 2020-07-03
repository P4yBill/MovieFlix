FROM python:3.6-slim
LABEL MAINTAINER="Vasilis Moraitis <v4s.moraitis@gmail.com>"

WORKDIR /app/flask

ADD . /app/flask
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python","-u", "app.py" ]