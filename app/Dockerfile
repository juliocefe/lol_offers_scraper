
FROM python:3.9.7-slim-buster

WORKDIR /app

COPY ./requirenments.txt .
RUN pip install -r requirenments.txt

COPY . .

CMD ["python", "offers.py"]