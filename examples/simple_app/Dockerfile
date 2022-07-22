FROM python:3.9-slim

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /app

COPY ./src .

ENV FLASK_APP app

EXPOSE 5000 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
