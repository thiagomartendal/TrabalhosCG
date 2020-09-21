from PyQt5.QtWidgets import *

class PainelLateral(QScrollArea):

    # Construtor
    def __init__(self):
        super(PainelLateral, self).__init__()
        self.__layoutPrincipal = QVBoxLayout()
        self.__zoom = 0
        self.__propriedades()
        self.__lista()
        self.__controlesWindow()

    # Primeiras definições do painel lateral
    def __propriedades(self):
        layout = QVBoxLayout()
        self.setMaximumWidth(self.width()*(0.4))
        self.setLayout(layout)
        grupo = QGroupBox()
        grupo.setTitle("Menu de Funções")
        grupo.setLayout(self.__layoutPrincipal)
        layout.addWidget(grupo)

    # Definições da lista gráfica para os objetos a serem criados
    def __lista(self):
        self.__listaObjetos = QListWidget()
        self.__listaObjetos.setMinimumWidth(900)
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Objetos")
        grupo.setLayout(layout)
        layout.addWidget(self.__listaObjetos)
        self.__layoutPrincipal.addWidget(grupo)

    # Definição dos botões de controle da window
    def __botoesWindow(self):
        self.__botoesControleWindow = [QPushButton("In"), QPushButton("Out"), QPushButton("Up"), QPushButton("Left"), QPushButton("Right"), QPushButton("Down")]
        self.__botoesControleWindow[0].setFixedWidth(45)
        self.__botoesControleWindow[1].setFixedWidth(45)
        self.__botoesControleWindow[2].setFixedWidth(45)
        self.__botoesControleWindow[3].setFixedWidth(45)
        self.__botoesControleWindow[4].setFixedWidth(45)
        self.__botoesControleWindow[5].setFixedWidth(45)

    # Define os componentes de controle para transformações na window e no viewport
    def __controlesWindow(self):
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Window")
        grupo.setLayout(layout)
        layoutPainel = QGridLayout()
        painel = QFrame()
        painel.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Faixa"), 0, 0)
        self.__entradaFaixa = QLineEdit()
        self.__entradaFaixa.setReadOnly(True)
        layoutPainel.addWidget(self.__entradaFaixa, 0, 1, 1, 3)
        self.__entradaFaixa.setText(str(self.__zoom))
        layoutPainel.addWidget(QLabel("%"), 0, 4)
        self.__botoesWindow()
        layoutPainel.addWidget(self.__botoesControleWindow[0], 1, 3)
        layoutPainel.addWidget(self.__botoesControleWindow[1], 3, 3)
        layoutPainel.addWidget(self.__botoesControleWindow[2], 1, 1)
        layoutPainel.addWidget(self.__botoesControleWindow[3], 2, 0)
        layoutPainel.addWidget(self.__botoesControleWindow[4], 2, 2)
        layoutPainel.addWidget(self.__botoesControleWindow[5], 3, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)

    def atualizarLista(self, objetos):
        self.__listaObjetos.clear()
        for objeto in objetos:
            if objeto.tipo() == 0:
                nome = objeto.getNome()+": Polígono"
            elif objeto.tipo() == 1:
                nome = objeto.getNome()+": Linha"
            elif objeto.tipo() == 2:
                nome = objeto.getNome()+": Ponto"
            self.__listaObjetos.addItem(nome)

    # Retorna a lista
    def getLista(self):
        return self.__listaObjetos

    # Retorna os botões de controle da window
    def getBotoesWindow(self):
        return self.__botoesControleWindow

    def setZoom(self, zoom):
        self.__zoom += zoom
        self.__entradaFaixa.setText(str(self.__zoom))
