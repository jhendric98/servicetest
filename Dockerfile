FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5002

CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "5002"]
