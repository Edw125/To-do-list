FROM python:3.11.4-slim

WORKDIR /

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python", "runner.py", "-m", "test"]
