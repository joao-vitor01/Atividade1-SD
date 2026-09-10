import grpc
from concurrent import futures
import uuid 
import os   
import tarefas_pb2
import tarefas_pb2_grpc

class GerenciadorDeTarefasServicer(tarefas_pb2_grpc.GerenciadorDeTarefasServicer):
    
    def __init__(self):
        self.pasta = "banco_de_tarefas"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta) 

    
    def CriarTarefa(self, request, context):
        print(f"Requisição recebida do cliente: {context.peer()}")
        
        novo_id = str(uuid.uuid4())
        
        caminho_arquivo = os.path.join(self.pasta, f"{novo_id}.txt")
        
        # Cria o arquivo e escreve os dados dentro dele
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"ID: {novo_id}\n")
            arquivo.write(f"Titulo: {request.titulo}\n")
            arquivo.write(f"Descricao: {request.descricao}\n")
            arquivo.write(f"Status: {request.status}\n")
            arquivo.write(f"Data Limite: {request.data_limite}\n")
   
            arquivo.write(f"Responsaveis: {', '.join(request.responsaveis)}\n")
            
        print(f"[SERVIDOR] Tarefa '{request.titulo}' criada com sucesso! ID salvo: {novo_id}")
        
        return tarefas_pb2.Tarefa(
            id=novo_id,
            titulo=request.titulo,
            descricao=request.descricao,
            status=request.status,
            data_limite=request.data_limite,
            responsaveis=request.responsaveis
        )


    def ListarTarefas(self, request, context):
        print("[SERVIDOR] O cliente pediu a lista de todas as tarefas...")
        print(f"Requisição recebida do cliente: {context.peer()}")
        
        tarefas_encontradas = []
        
        if os.path.exists(self.pasta):
            for nome_arquivo in os.listdir(self.pasta):
                if nome_arquivo.endswith(".txt"):
                    caminho_arquivo = os.path.join(self.pasta, nome_arquivo)
                    
                    # Lê o arquivo de texto linha por linha para recuperar os dados
                    dados = {}
                    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                        for linha in arquivo:
                            if ":" in linha:
                                chave, valor = linha.strip().split(":", 1)
                                dados[chave.strip()] = valor.strip()
                    
                    # Monta o objeto Tarefa usando o modelo do Protobuf
                    tarefa_obj = tarefas_pb2.Tarefa(
                        id=dados.get("ID", ""),
                        titulo=dados.get("Titulo", ""),
                        descricao=dados.get("Descricao", ""),
                        status=dados.get("Status", ""),
                        data_limite=dados.get("Data Limite", ""),
                        responsaveis=dados.get("Responsaveis", "").split(", ") if dados.get("Responsaveis") else []
                    )
                    tarefas_encontradas.append(tarefa_obj)

        print(f"[SERVIDOR] Encontradas {len(tarefas_encontradas)} tarefas salvas.")
        
       
        return tarefas_pb2.ListaTarefasResponse(tarefas=tarefas_encontradas)


    def AtualizarTarefa(self, request, context):
        print(f"Requisição recebida do cliente: {context.peer()}")
        caminho_arquivo = os.path.join(self.pasta, f"{request.id}.txt")
        
        
        if not os.path.exists(caminho_arquivo):
            print(f"[SERVIDOR] Erro: Tarefa com ID {request.id} não foi encontrada para atualização.")
            return tarefas_pb2.Tarefa() # Retorna vazio se não achar
            
       
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"ID: {request.id}\n")
            arquivo.write(f"Titulo: {request.titulo}\n")
            arquivo.write(f"Descricao: {request.descricao}\n")
            arquivo.write(f"Status: {request.status}\n")
            arquivo.write(f"Data Limite: {request.data_limite}\n")
            arquivo.write(f"Responsaveis: {', '.join(request.responsaveis)}\n")
            
        print(f"[SERVIDOR] Tarefa com ID '{request.id}' atualizada com sucesso!")
        
        
        return request



    def DeletarTarefa(self, request, context):
        
        print(f"Requisição recebida do cliente: {context.peer()}")
        caminho_arquivo = os.path.join(self.pasta, f"{request.id}.txt")
        
        # Verifica se o arquivo realmente existe antes de tentar apagar
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo) # Apaga o arquivo físico do computador
            print(f"[SERVIDOR] Tarefa com ID '{request.id}' foi deletada com sucesso!")
        else:
            print(f"[SERVIDOR] Aviso: Tentou deletar o ID {request.id}, mas o arquivo não foi encontrado.")
            
        return tarefas_pb2.Empty()




    
def iniciar_servidor():
    # Prepara o servidor para aguentar até 10 conexões simultâneas
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    tarefas_pb2_grpc.add_GerenciadorDeTarefasServicer_to_server(
        GerenciadorDeTarefasServicer(), servidor
    )
    
    # Define a porta padrão do gRPC (50051)
    servidor.add_insecure_port('[::]:50051')
    
    print("[SERVIDOR] Servidor online! Escutando requisições na porta 50051...")
    
    # Liga e fica esperando infinitamente
    servidor.start()
    servidor.wait_for_termination()

# Executa o código
if __name__ == '__main__':
    iniciar_servidor()