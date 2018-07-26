FROM python:3.6-slim

WORKDIR /csv-to-dialogflow-intent

ADD . /csv-to-dialogflow-intent

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

