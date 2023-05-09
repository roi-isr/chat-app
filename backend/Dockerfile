FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip3.11 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["bash", "scripts/entrypoint.sh", "8080"]
