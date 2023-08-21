FROM python:3.8-slim

WORKDIR /

COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
