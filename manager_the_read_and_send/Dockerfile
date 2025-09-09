FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY loger/ ./loger
COPY manager_the_read_and_send/ .
COPY utils/ ./utils

CMD ["python", "manager.py"]
