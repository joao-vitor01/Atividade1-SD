# Atividade de Sistemas Distribuídos 

- **Versão do python usada:** `Python 3.11.9`
- **Pacote Python necessário:** `grpcio-tools`

## Como rodar via Docker

### 1. Build das imagens(primeira vez)


    docker compose build

### 2. Iniciar o Servidor

    docker compose up servidor

- O terminal ficará ocupado exibindo os logs do servidor.
Abra novos terminais para os próximos passos.


### 3. Iniciar o cliente 1(em outro terminal)


    docker compose run cliente_1


### 4. Iniciar o cliente 2(em outro terminal)


    docker compose run cliente_2


### Para ver os IPs atribuídos

    docker network inspect atividade1-sd_rede_tarefas

## Rodando localmente (sem Docker)

Se preferir rodar sem Docker, instale as dependências:


    pip install -r requirements.txt


 - Sempre que houver alteração no contrato de serviço, é necessário recompilar o arquivo `tarefas.proto`. Execute o comando abaixo na raiz do projeto para gerar `tarefas_pb2_grpc.py` e `tarefas_pb2.py`:

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefas.proto


Depois rode `servidor.py` e `cliente.py` normalmente.