"""
SysInfoDashboard
----------------
Uma aplicação GUI em PyQt5 para exibir informações detalhadas do sistema, como detalhes de CPU, memória e armazenamento,
bem como o status da conexão de rede e a data/hora atual.

Dependências:
- PyQt5
- psutil
- requests

Importação de módulos:
- sys: Para manipulação de argumentos e saída padrão.
- platform: Para obter informações sobre o sistema operacional.
- psutil: Para obter informações sobre o uso do sistema (CPU, memória, armazenamento).
- datetime: Para manipular e formatar data e hora.
- requests: Para verificar a conexão com a internet.
- PyQt5.QtWidgets: Para criar a interface gráfica.
- PyQt5.QtCore: Para temporizador e manipulação de eventos.
"""

import sys
import platform
import psutil
import datetime
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer

def mostrar_informacoes_do_sistema():
    """
    Obtém informações detalhadas sobre o sistema, incluindo CPU, memória e armazenamento.
    
    Retorna:
        list: Uma lista de listas contendo descrições e valores das informações do sistema.
    """
    info = []

    # Informações básicas do sistema
    info.append(["Nome do sistema", platform.system()])
    info.append(["Versão do sistema", platform.version()])
    info.append(["Nome da máquina", platform.node()])
    info.append(["Arquitetura", platform.architecture()[0]])
    info.append(["Processador", platform.processor()])

    # Informações de CPU
    info.append(["Uso da CPU (%)", f"{psutil.cpu_percent(interval=1)}"])
    info.append(["Núcleos lógicos", psutil.cpu_count(logical=True)])
    info.append(["Núcleos físicos", psutil.cpu_count(logical=False)])

    # Informações de Memória
    mem = psutil.virtual_memory()
    info.append(["Memória Total (GB)", f"{mem.total / (1024**3):.2f}"])
    info.append(["Memória Disponível (GB)", f"{mem.available / (1024**3):.2f}"])
    info.append(["Uso de Memória (%)", mem.percent])

    # Informações de Armazenamento
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        info.append(["Dispositivo", part.device])
        info.append(["Ponto de montagem", part.mountpoint])
        info.append(["Tipo de sistema de arquivos", part.fstype])
        info.append(["Tamanho Total (GB)", f"{usage.total / (1024**3):.2f}"])
        info.append(["Espaço Usado (GB)", f"{usage.used / (1024**3):.2f}"])
        info.append(["Espaço Livre (GB)", f"{usage.free / (1024**3):.2f}"])
        info.append(["Uso (%)", usage.percent])

    return info

def verificar_conexao():
    """
    Verifica a conexão com a internet tentando acessar o Google.
    
    Retorna:
        str: "Conectado" se a conexão for bem-sucedida, caso contrário, retorna "Desconectado".
    """
    try:
        response = requests.get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            return "Conectado"
    except requests.ConnectionError:
        return "Desconectado"
    return "Desconectado"

class MainWindow(QMainWindow):
    """
    A classe principal da janela da aplicação que exibe as informações do sistema.
    """

    def __init__(self):
        """
        Inicializa a janela principal e configura o layout, widgets e temporizador.
        """
        super().__init__()
        self.setWindowTitle("Informações do Sistema")
        self.setGeometry(100, 100, 1200, 800)  # Ajuste o tamanho inicial da janela

        # Criar o widget central e layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Adicionar a barra superior com data e diretório inicial
        self.top_bar = QWidget()
        self.top_bar_layout = QVBoxLayout(self.top_bar)
        self.date_label = QLabel()
        self.home_label = QLabel()
        self.network_label = QLabel()
        self.top_bar_layout.addWidget(self.date_label)
        self.top_bar_layout.addWidget(self.home_label)
        self.top_bar_layout.addWidget(self.network_label)
        layout.addWidget(self.top_bar)

        # Criar o widget de tabela
        self.table_widget = QTableWidget()
        self.populate_table()

        # Adicionar widgets ao layout
        layout.addWidget(self.table_widget)

        # Configurar e iniciar o timer para atualizar a data e a hora e verificar a conexão
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # Atualiza a cada 1 segundo

        # Atualizar o status inicial
        self.update_status()

    def update_status(self):
        """
        Atualiza os rótulos de data/hora, diretório inicial e status da conexão de rede.
        """
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y %H:%M:%S")
        home_dir = platform.node()  # ou `os.path.expanduser("~")` para diretório home
        network_status = verificar_conexao()

        self.date_label.setText(f"Data e Hora: {date_str}")
        self.home_label.setText(f"Diretório Inicial: {home_dir}")
        self.network_label.setText(f"Status da Rede: {network_status}")

    def populate_table(self):
        """
        Preenche a tabela com as informações do sistema obtidas pela função `mostrar_informacoes_do_sistema`.
        """
        info = mostrar_informacoes_do_sistema()
        
        # Configurar o número de linhas e colunas
        self.table_widget.setRowCount(len(info))
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Descrição", "Valor"])
        
        # Adicionar dados à tabela
        for row, (desc, valor) in enumerate(info):
            self.table_widget.setItem(row, 0, QTableWidgetItem(desc))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(valor)))

        # Ajustar a largura das colunas proporcionalmente
        self.table_widget.resizeColumnsToContents()
        header = self.table_widget.horizontalHeader()
        total_width = self.table_widget.width()
        column_count = self.table_widget.columnCount()
        
        if column_count > 0:
            default_width = total_width // column_count + 200
            for col in range(column_count):
                header.resizeSection(col, default_width)

def main():
    """
    Função principal para iniciar a aplicação PyQt5.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
