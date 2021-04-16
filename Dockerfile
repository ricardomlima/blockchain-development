FROM python:3.8.8


COPY ./workplace/ /home/

WORKDIR /home/

RUN pip install -r requirements.txt

EXPOSE 8888
EXPOSE 8000
EXPOSE 5000

CMD FLASK_APP=app.py flask run