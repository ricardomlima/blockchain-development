FROM python:3.8.8


COPY ./workplace/ /home/

WORKDIR /home/

RUN pip install -r requirements.txt

CMD FLASK_APP=app.py flask run