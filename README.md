# Atividade de Sistemas Distribuídos 

- **Versão do python usada:** `Python 3.11.9`

- **Pacote Python necessário:** 

biblioteca necessária para compilar `tarefas.proto`:

    pip install grpcio-tools


- **Compilação de `tarefas.proto`:** Sempre que houver alteração no contrato de serviço, é necessário recompilar o arquivo .proto.

Execute o comando abaixo na raiz do projeto para gerar `tarefas_pb2_grpc.py` e `tarefas_pb2.py`:

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefas.proto
