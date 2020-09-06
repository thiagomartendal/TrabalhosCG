from PyQt5.QtWidgets import *
from interface.inserir.montarPoligono import *
from interface.inserir.montarReta import *
from interface.inserir.montarPonto import *
from objeto.poligono import *
from objeto.linha import *
from objeto.ponto import *
from objeto.estruturaPonto import *

class InserirObjeto(QDialog):
    __coordenadas = [] # Coordenadas para formar pontos do objeto

    # Construtor
    def __init__(self, tipo, parent=None):
        super(InserirObjeto, self).__init__()
        self.setWindowTitle("Inserir Objeto")
        self.setFixedSize(500, 230)
        self.__tipo = tipo
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.__nomeForma())
        self.__sinalBotao = -1
        if self.__tipo == 0:
            mpol = MontarPoligono()
            layout.addWidget(mpol)
            self.__coordenadas = mpol.coordenadas()
        elif self.__tipo == 1:
            mret = MontarReta();
            layout.addWidget(mret)
            self.__coordenadas = mret.coordenadas()
        elif self.__tipo == 2:
            mpon = MontarPonto()
            layout.addWidget(mpon)
            self.__coordenadas = mpon.coordenadas()
        self.__botoes(layout)

    # Método par nomear o objeto
    def __nomeForma(self):
        layoutPainel = QHBoxLayout()
        painel = QFrame()
        painel.setLayout(layoutPainel)
        nome = QLineEdit()
        layoutPainel.addWidget(QLabel("Nome da Forma: "))
        layoutPainel.addWidget(nome)
        self.__nomeObjeto = nome
        return painel

    # Botões de interação
    def __botoes(self, layout):
        botaoOk = QPushButton("Ok")
        botaoOk.clicked.connect(lambda: self.__ok())
        botaoCancelar = QPushButton("Cancelar")
        botaoCancelar.clicked.connect(lambda: self.__cancelar())
        layoutPainel = QHBoxLayout()
        painel = QFrame()
        painel.setLayout(layoutPainel)
        layoutPainel.addWidget(botaoOk)
        layoutPainel.addWidget(botaoCancelar)
        layout.addWidget(painel)

    # Ação do botão OK
    def __ok(self):
        nome = self.__nomeObjeto.text()
        tmpC = []
        if self.__tipo == 0:
            tmpC = self.__coordenadas[0].text().split(' ')
        else:
            tmpC = self.__coordenadas
        pontos = []
        for i in range(0, len(tmpC)):
            if i % 2 != 0:
                str1 = tmpC[i-1] if self.__tipo == 0 else tmpC[i-1].text()
                str2 = tmpC[i] if self.__tipo == 0 else tmpC[i].text()
                p = EstruturaPonto(float(str1), float(str2))
                pontos.append(p)
                i+1
        tmpC.clear()
        if self.__tipo == 0:
            if len(pontos) % 2 == 0:
                self.__objeto = Poligono(nome, pontos)
                self.__sinalBotao = 0
            else:
                QMessageBox.question(self, 'Atenção', 'Digite um número par de coordenadas para formar os pontos.', QMessageBox.Ok)
        elif self.__tipo == 1:
            self.__objeto = Linha(nome, pontos)
            self.__sinalBotao = 0
        if self.__tipo == 2:
            self.__objeto = Ponto(nome, pontos)
            self.__sinalBotao = 0
        if self.__sinalBotao == 0:
            self.hide()

    # Ação do botão Cancelar
    def __cancelar(self):
        self.__sinalBotao = 1
        self.hide()
        self.destroy()

    # Retorno do objeto criado
    def getObj(self):
        return self.__objeto

    # Retorna o Sinal
    def getSinal(self):
        return self.__sinalBotao
