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
        self.__selecaoEixo()
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
        self.__botoesControleWindow = [QPushButton("In"),
                                       QPushButton("Out"),
                                       QPushButton("Up"),
                                       QPushButton("Left"),
                                       QPushButton("Right"),
                                       QPushButton("Down"),
                                       QPushButton("Forward"),
                                       QPushButton("Back")]
        self.__botoesControleWindow[0].setFixedWidth(45)
        self.__botoesControleWindow[1].setFixedWidth(45)
        self.__botoesControleWindow[2].setFixedWidth(45)
        self.__botoesControleWindow[3].setFixedWidth(45)
        self.__botoesControleWindow[4].setFixedWidth(45)
        self.__botoesControleWindow[5].setFixedWidth(45)
        self.__botoesControleWindow[6].setFixedWidth(55)
        self.__botoesControleWindow[7].setFixedWidth(55)

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
        layoutPainel.addWidget(self.__botoesControleWindow[6], 4, 0)
        layoutPainel.addWidget(self.__botoesControleWindow[7], 4, 2)
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
        self.__entradaDz = QLineEdit()
        layoutPainel.addWidget(QLabel("Dz"), 2, 0)
        self.__entradaDz.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaDz, 2, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesTranslacao()
        tl = QLabel("Transladar Objeto:")
        tl.setFixedWidth(105)
        layoutPainel.addWidget(tl, 3, 1)
        layoutPainel.addWidget(self.__botoesControleTranslacao[0], 4, 1)
        layoutPainel.addWidget(self.__botoesControleTranslacao[1], 4, 2)

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
        layoutPainel.addWidget(QLabel("Sy"), 1, 0)
        self.__entradaSy = QLineEdit()
        self.__entradaSy.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaSy, 1, 1)
        layoutPainel.addWidget(QLabel("Sz"), 2, 0)
        self.__entradaSz = QLineEdit()
        self.__entradaSz.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaSz, 2, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesEscalonamento()
        layoutPainel.addWidget(self.__botoesControleEscalonamento[0], 3, 1)

    # Define os componentes de selecao de eixo
    def __selecaoEixo(self):
        layout = QVBoxLayout()
        grupo = QGroupBox()
        grupo.setTitle("Eixo")
        grupo.setLayout(layout)
        layoutPainel = QGridLayout()
        painel = QFrame()
        painel.setMaximumWidth(self.width()-75)
        painel.setLayout(layoutPainel)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        #
        self.__botoesEixo = [QPushButton("X"), QPushButton("Y"), QPushButton("Z")]
        self.__botoesEixo[0].setStyleSheet("background-color: red")
        self.__botoesEixo[1].setStyleSheet("background-color: lightgreen")
        self.__botoesEixo[2].setStyleSheet("background-color: lightblue")
        self.__eixoAtualLabel = QLabel("Eixo Atual: Z")
        self.__eixoAtualLabel.setFixedWidth(105)
        layoutPainel.addWidget(self.__eixoAtualLabel, 1, 1)
        layoutPainel.addWidget(self.__botoesEixo[0], 2, 1)
        layoutPainel.addWidget(self.__botoesEixo[1], 2, 2)
        layoutPainel.addWidget(self.__botoesEixo[2], 2, 3)

    # Definição dos botões de controle da rotação
    def __botoesRotacao(self):
        self.__botoesControleRotacao = [QPushButton("Eixo"),
                                        QPushButton("Centro do Mundo"),
                                        QPushButton("Centro do Objeto"),
                                        QPushButton("Ponto Qualquer"),
                                        QPushButton("Window a Esquerda"),
                                        QPushButton("Window a Direita")]

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
        layoutPainel.addWidget(QLabel("Z"), 3, 0)
        self.__entradaZ = QLineEdit()
        self.__entradaZ.setFixedWidth(120)
        layoutPainel.addWidget(self.__entradaZ, 3, 1)
        layout.addWidget(painel)
        self.__layoutPrincipal.addWidget(grupo)
        self.__botoesRotacao()
        layoutPainel.addWidget(QLabel("Rotacionar:"), 4, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[0], 5, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[1], 6, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[2], 7, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[3], 8, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[4], 9, 1)
        layoutPainel.addWidget(self.__botoesControleRotacao[5], 10, 1)

    # Atualiza a lista de objetos criados
    def atualizarLista(self, objetos):
        self.__listaObjetos.clear()
        nomeTipos = {
                    0: "Polígono",
                    1: "Linha",
                    2: "Ponto",
                    3: "CurvaBezier",
                    4: "BSpline",
                    5: "Modelo de Arame",
                    6: "Superfície Bicúbica"
                     }
        for objeto in objetos:
            nome = objeto.getNome()+": "+nomeTipos[objeto.tipo()]
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
        dx = self.__entradaDx.text() if self.__entradaDx.text() else 0
        dy = self.__entradaDy.text() if self.__entradaDy.text() else 0
        dz = self.__entradaDz.text() if self.__entradaDz.text() else 0
        return [self.__posItem, float(dx), float(dy), float(dz)]

    # Retorna os botões de controle do escalonamento
    def getBotoesEscalonamento(self):
        return self.__botoesControleEscalonamento

    # Retorna os valores do escalonamento
    def getValoresEscalonamento(self):
        sx = self.__entradaSx.text() if self.__entradaSx.text() else 1
        sy = self.__entradaSy.text() if self.__entradaSy.text() else 1
        sz = self.__entradaSz.text() if self.__entradaSz.text() else 1
        return [self.__posItem, float(sx), float(sy), float(sz)]

    # Retorna os botões de controle da rotação
    def getBotoesRotacao(self):
        return self.__botoesControleRotacao

    # Retorna os valores da rotação
    def getValoresRotacao(self):
        angulo = self.__entradaAngulo.text()
        x = self.__entradaX.text()
        y = self.__entradaY.text()
        z = self.__entradaZ.text()
        angulo = angulo if angulo else 0
        x = x if x else 0
        y = y if y else 0
        z = z if z else 0
        return [self.__posItem, float(angulo), float(x), float(y), float(z)]

    # Retorna os botões de selecao do Eixo
    def getBotoesEixo(self):
        return self.__botoesEixo

    def setEixoAtual(self, eixo):
        self.__eixoAtualLabel.setText("Eixo Atual: " + eixo)
