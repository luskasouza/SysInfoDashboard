import platform
import datetime
import time

class ExecutionInfo:
    def __init__(self):
        self.data_execucao = self.obter_data_execucao()
        self.inicio = None
        self.fim = None

    def obter_data_execucao(self):
        return datetime.datetime.now()

    def iniciar_execucao(self):
        self.inicio = time.time()

    def finalizar_execucao(self):
        self.fim = time.time()

    def calcular_tempo_execucao(self):
        if self.inicio is not None and self.fim is not None:
            return self.fim - self.inicio
        return None

    def obter_sistema_operacional(self):
        return f'{platform.system()}-{platform.release()}'

    def imprimir_info(self):
        tempo_execucao = self.calcular_tempo_execucao()
        print('=================================================================')
        print(f'SISTEMA OPERACIONAL: {self.obter_sistema_operacional()}')
        print(f'DATA DE EXECUÇÃO: {self.data_execucao.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'TEMPO DE EXECUÇÃO: {tempo_execucao:.2f} segundos' if tempo_execucao is not None else "TEMPO DE EXECUÇÃO")
        print('=================================================================')
