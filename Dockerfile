# Usa a versão exata do Python que você definiu no README
FROM python:3.11.9-slim

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala as dependências (grpcio e grpcio-tools)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os seus arquivos (servidor.py, cliente.py, .proto, etc)
COPY . .

#compila o .proto dentro do contênier para gerar os arquivos pb2 e pb2_grpc
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefas.proto