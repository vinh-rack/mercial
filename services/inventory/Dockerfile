FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY services/inventory/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared ./shared
COPY services/inventory/ .

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. inventory.proto

CMD ["python", "main.py"]
