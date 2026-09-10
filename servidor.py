import grpc
from concurrent import futures
import uuid 
import os   
import tarefas_pb2
import tarefas_pb2_grpc

# 1. A NOSSA COZINHA (O Servidor)
class GerenciadorDeTarefasServicer(tarefas_pb2_grpc.GerenciadorDeTarefasServicer):
    
    def __init__(self):
        # O professor pediu para salvar em uma pasta específica
        self.pasta = "banco_de_tarefas"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta) # Se a pasta não existir, cria ela agora

    # 2. A FUNÇÃO DE CRIAR TAREFA
    def CriarTarefa(self, request, context):
        # AQUI O GPRC JÁ DESAMASSOU O BINÁRIO! 
        # O 'request' já é um objeto Python normal com os dados do cliente.
        
        # Gera o ID único usando UUID
        novo_id = str(uuid.uuid4())
        
        # Monta o nome do arquivo de texto (Ex: banco_de_tarefas/123-456.txt)
        caminho_arquivo = os.path.join(self.pasta, f"{novo_id}.txt")
        
        # Cria o arquivo e escreve os dados dentro dele
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"ID: {novo_id}\n")
            arquivo.write(f"Titulo: {request.titulo}\n")
            arquivo.write(f"Descricao: {request.descricao}\n")
            arquivo.write(f"Status: {request.status}\n")
            arquivo.write(f"Data Limite: {request.data_limite}\n")
            # Como responsaveis é um 'repeated' (lista), juntamos com vírgula
            arquivo.write(f"Responsaveis: {', '.join(request.responsaveis)}\n")
            
        print(f"[SERVIDOR] Tarefa '{request.titulo}' criada com sucesso! ID salvo: {novo_id}")
        
        # AQUI VAMOS AMASSAR PARA BINÁRIO NOVAMENTE!
        # Usamos o tarefas_pb2 para montar a Resposta. Quando dermos o 'return', 
        # o gRPC vai amassar isso e enviar pela rede.
        return tarefas_pb2.Tarefa(
            id=novo_id,
            titulo=request.titulo,
            descricao=request.descricao,
            status=request.status,
            data_limite=request.data_limite,
            responsaveis=request.responsaveis
        )

# 3. A FUNÇÃO DE LISTAR TAREFAS
    def ListarTarefas(self, request, context):
        print("[SERVIDOR] O cliente pediu a lista de todas as tarefas...")
        
        # Cria uma lista vazia para guardar as tarefas encontradas
        tarefas_encontradas = []
        
        # Pega todos os arquivos dentro da pasta do "banco de dados"
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
        
        # Devolve a lista completa empacotada no formato que o .proto definiu
        return tarefas_pb2.ListaTarefasResponse(tarefas=tarefas_encontradas)

    
    # 4. A FUNÇÃO DE ATUALIZAR TAREFA
    def AtualizarTarefa(self, request, context):
        # Localiza o arquivo exato usando o ID que veio na requisição
        caminho_arquivo = os.path.join(self.pasta, f"{request.id}.txt")
        
        # Verifica se o arquivo realmente existe na pasta
        if not os.path.exists(caminho_arquivo):
            print(f"[SERVIDOR] Erro: Tarefa com ID {request.id} não foi encontrada para atualização.")
            return tarefas_pb2.Tarefa() # Retorna vazio se não achar
            
        # Abre o arquivo no modo "w" (write), o que sobrescreve tudo o que estava escrito antes
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"ID: {request.id}\n")
            arquivo.write(f"Titulo: {request.titulo}\n")
            arquivo.write(f"Descricao: {request.descricao}\n")
            arquivo.write(f"Status: {request.status}\n")
            arquivo.write(f"Data Limite: {request.data_limite}\n")
            arquivo.write(f"Responsaveis: {', '.join(request.responsaveis)}\n")
            
        print(f"[SERVIDOR] Tarefa com ID '{request.id}' atualizada com sucesso!")
        
        # Devolve a própria requisição modificada de volta para confirmar a alteração
        return request



# 5. A FUNÇÃO DE DELETAR TAREFA
    def DeletarTarefa(self, request, context):
        # Monta o caminho do arquivo usando o ID que veio na requisição de exclusão
        caminho_arquivo = os.path.join(self.pasta, f"{request.id}.txt")
        
        # Verifica se o arquivo realmente existe antes de tentar apagar
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo) # Apaga o arquivo físico do computador
            print(f"[SERVIDOR] Tarefa com ID '{request.id}' foi deletada com sucesso!")
        else:
            print(f"[SERVIDOR] Aviso: Tentou deletar o ID {request.id}, mas o arquivo não foi encontrado.")
            
        # Como o .proto define que DeletarTarefa retorna um Empty, devolvemos um objeto vazio
        return tarefas_pb2.Empty()




    
# 3. LIGANDO O SERVIDOR NA TOMADA
def iniciar_servidor():
    # Prepara o servidor para aguentar até 10 conexões simultâneas
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Avisa ao gRPC que a classe que criamos ali em cima é a que vai responder as requisições
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