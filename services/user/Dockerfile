FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY services/user/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared ./shared
COPY services/user/ .

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto

CMD ["python", "main.py"]
