from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class PainelLateral(QScrollArea):

    # Construtor
    def __init__(self):
        super(PainelLateral, self).__init__()
        self.__layoutPrincipal = QVBoxLayout()
        self.__zoom = 0
        self.__posItem = -1
        self.__propriedades()
        self.__lista()
        self.__controlesWindow()
        self.__controlesTranslacao()
        self.__controlesEscalonamento()
        self.__controlesRotacao()
        self.__listaObjetos.clicked.connect(lambda: self.__itemSelecionado())

    # Primeiras definições do painel lateral
    def __propriedades(self):
        layout = QVBoxLayout()
        self.setMaximumWidth(self.width()*(0.4))
        grupo = QGroupBox()
        grupo.setTitle("Menu de Funções")
        grupo.setLayout(self.__layoutPrincipal)
        layout.addWidget(grupo)
        self.setWidget(grupo)
        self.setWidgetResizable(True)

    # Definições da lista gráfica para os objetos a serem criados
    def __lista(self):
        self.__listaObjetos = QListWidget()
        self.__listaObjetos.setMaximumWidth(self.width()-75)
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Objetos")
        grupo.setLayout(layout)
        painel = QFrame()
        painel.setFixedHeight(400)
        layoutPainel = QVBoxLayout()
        layoutPainel.addWidget(self.__listaObjetos)
        painel.setLayout(layoutPainel)
        layout.addWidget(painel)
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
        painel.setMaximumWidth(self.width()-75)
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

    # Definição dos botões de controle da translação
    def __botoesTranslacao(self):
        self.__botoesControleTranslacao = [QPushButton("Todos"), QPushButton("Selecionado")]
        self.__botoesControleTranslacao[1].setFixedWidth(77)

    # Define os componentes de controle da translação
    def __controlesTranslacao(self):
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Translação")
        grupo.setLayout(layout)
        layoutPainel = QGridLayout()
        painel = QFrame()
        painel.setMaximumWidth(self.width()-75)
        painel.setLayout(layoutPainel)
        self.__entradaDx = QLineEdit()
        layoutPainel.addWidget(QLabel("Dx"), 0, 0)
        self.__entradaDx.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaDx, 0, 1)
        self.__entradaDy = QLineEdit()
        layoutPainel.addWidget(QLabel("DY"), 1, 0)
        self.__entradaDy.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaDy, 1, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesTranslacao()
        tl = QLabel("Transladar Objeto:")
        tl.setFixedWidth(105)
        layoutPainel.addWidget(tl, 2, 1)
        layoutPainel.addWidget(self.__botoesControleTranslacao[0], 3, 1)
        layoutPainel.addWidget(self.__botoesControleTranslacao[1], 3, 2)

    # Definição dos botões de controle do escalonamento
    def __botoesEscalonamento(self):
        self.__botoesControleEscalonamento = [QPushButton("Escalonar Objeto")]
        # self.__botoesControleEscalonamento[0].setFixedWidth(105)

    # Define os componentes de controle do escalonamento
    def __controlesEscalonamento(self):
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Escalonamento")
        grupo.setLayout(layout)
        layoutPainel = QGridLayout()
        painel = QFrame()
        painel.setMaximumWidth(self.width()-75)
        painel.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Sx"), 0, 0)
        self.__entradaSx = QLineEdit()
        self.__entradaSx.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaSx, 0, 1)
        layoutPainel.addWidget(QLabel("SY"), 1, 0)
        self.__entradaSy = QLineEdit()
        self.__entradaSy.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaSy, 1, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesEscalonamento()
        layoutPainel.addWidget(self.__botoesControleEscalonamento[0], 2, 1)

    # Definição dos botões de controle da rotação
    def __botoesRotacao(self):
        self.__botoesControleRotacao = [QPushButton("Centro do Mundo"), QPushButton("Centro do Objeto"), QPushButton("Ponto Qualquer"), QPushButton("Window a Esquerda"), QPushButton("Window a Direita")]

    # Define os componentes de controle da rotação
    def __controlesRotacao(self):
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Rotação")
        grupo.setLayout(layout)
        layoutPainel = QGridLayout()
        painel = QFrame()
        painel.setMaximumWidth(self.width()-75)
        painel.setFixedWidth(190)
        painel.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Ângulo"), 0, 0)
        self.__entradaAngulo = QLineEdit()
        self.__entradaAngulo.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaAngulo, 0, 1)
        layoutPainel.addWidget(QLabel("X"), 1, 0)
        self.__entradaX = QLineEdit()
        self.__entradaX.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaX, 1, 1)
        layoutPainel.addWidget(QLabel("Y"), 2, 0)
        self.__entradaY = QLineEdit()
        self.__entradaY.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaY, 2, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesRotacao()
        layoutPainel.addWidget(QLabel("Rotacionar:"), 3, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[0], 4, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[1], 5, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[2], 6, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[3], 7, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[4], 8, 1)

    # Atualiza a lista de objetos criados
    def atualizarLista(self, objetos):
        self.__listaObjetos.clear()
        for objeto in objetos:
            if objeto.tipo() == 0:
                nome = objeto.getNome()+": Polígono"
            elif objeto.tipo() == 1:
                nome = objeto.getNome()+": Linha"
            elif objeto.tipo() == 2:
                nome = objeto.getNome()+": Ponto"
            elif objeto.tipo() == 3:
                nome = objeto.getNome()+": CurvaBezier"
            elif objeto.tipo() == 4:
                nome = objeto.getNome()+": BSpline"
            self.__listaObjetos.addItem(nome)

    # Seleciona o índice do objeto selecionado
    def __itemSelecionado(self):
        self.__posItem = self.__listaObjetos.row(self.__listaObjetos.currentItem())

    # Entrada do zoom
    def setZoom(self, zoom):
        self.__zoom += zoom
        self.__entradaFaixa.setText(str(self.__zoom))

    # Retorna a lista
    def getLista(self):
        return self.__listaObjetos

    # Retorna os botões de controle da window
    def getBotoesWindow(self):
        return self.__botoesControleWindow

    # Retorna os botões de aplicação da translação
    def getBotoesTranslacao(self):
        return self.__botoesControleTranslacao

    # Retorna os valores da translação
    def getValoresTranslacao(self):
        return [self.__posItem, float(self.__entradaDx.text()), float(self.__entradaDy.text())]

    # Retorna os botões de controle do escalonamento
    def getBotoesEscalonamento(self):
        return self.__botoesControleEscalonamento

    # Retorna os valores do escalonamento
    def getValoresEscalonamento(self):
        return [self.__posItem, float(self.__entradaSx.text()), float(self.__entradaSy.text())]

    # Retorna os botões de controle da rotação
    def getBotoesRotacao(self):
        return self.__botoesControleRotacao

    # Retorna os valores da rotação
    def getValoresRotacao(self):
        x = self.__entradaX.text()
        y = self.__entradaY.text()
        if x == "":
            x = 0
        if y == "":
            y = 0
        return [self.__posItem, float(self.__entradaAngulo.text()), float(x), float(y)]
