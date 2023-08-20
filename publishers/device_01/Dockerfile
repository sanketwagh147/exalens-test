FROM python:3.8-slim

WORKDIR /sensor

COPY sensor /sensor/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
