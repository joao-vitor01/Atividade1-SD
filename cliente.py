import grpc
import tarefas_pb2
import tarefas_pb2_grpc

import grpc
import tarefas_pb2
import tarefas_pb2_grpc

def executar_cliente():
    # ATENÇÃO PARA O VIRTUALBOX: 
    # Quando for testar com a máquina virtual, troque 'localhost' pelo IP do VirtualBox (ex: '192.168.56.10')
    endereco_servidor = 'localhost:50051'
    
    print(f"Conectando ao servidor em {endereco_servidor}...")
    
    with grpc.insecure_channel(endereco_servidor) as canal:
        stub = tarefas_pb2_grpc.GerenciadorDeTarefasStub(canal)
        
        while True:
            print("\n====================")
            print(" GERENCIADOR DE TAREFAS ")
            print("====================")
            print("1. Criar Tarefa")
            print("2. Listar Tarefas")
            print("3. Atualizar Tarefa")
            print("4. Deletar Tarefa")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                titulo = input("Título: ")
                descricao = input("Descrição: ")
                status = input("Status: ")
                data_limite = input("Data limite: ")
                responsaveis = input("Responsáveis (separados por vírgula): ").split(",")
                responsaveis = [r.strip() for r in responsaveis]
                
                pedido = tarefas_pb2.CriarTarefaRequest(
                    titulo=titulo, descricao=descricao, status=status,
                    data_limite=data_limite, responsaveis=responsaveis
                )
                resposta = stub.CriarTarefa(pedido)
                print(f"\n[SUCESSO] Tarefa criada! ID: {resposta.id}")
                
            elif opcao == "2":
                print("\nBuscando tarefas no servidor...")
                resposta = stub.ListarTarefas(tarefas_pb2.Empty())
                for t in resposta.tarefas:
                    print(f"----------------------------------")
                    print(f"ID: {t.id}")
                    print(f"Título: {t.titulo} | Status: {t.status}")
                    print(f"Descrição: {t.descricao}")
                    print(f"Data Limite: {t.data_limite}")
                    print(f"Responsáveis: {', '.join(t.responsaveis)}")
                print(f"----------------------------------")
                
            elif opcao == "3":
                id_tarefa = input("Digite o ID exato da tarefa que deseja atualizar: ")
                titulo = input("Novo Título: ")
                descricao = input("Nova Descrição: ")
                status = input("Novo Status: ")
                data_limite = input("Nova Data limite: ")
                responsaveis = input("Novos Responsáveis (separados por vírgula): ").split(",")
                responsaveis = [r.strip() for r in responsaveis]
                
                pedido = tarefas_pb2.Tarefa(
                    id=id_tarefa, titulo=titulo, descricao=descricao, status=status,
                    data_limite=data_limite, responsaveis=responsaveis
                )
                stub.AtualizarTarefa(pedido)
                print("\n[SUCESSO] Tarefa atualizada!")
                
            elif opcao == "4":
                id_tarefa = input("Digite o ID da tarefa que deseja deletar: ")
                pedido = tarefas_pb2.TarefaIdRequest(id=id_tarefa)
                stub.DeletarTarefa(pedido)
                print("\n[SUCESSO] Tarefa removida do servidor!")
                
            elif opcao == "0":
                print("Encerrando cliente...")
                break
            else:
                print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    executar_cliente()