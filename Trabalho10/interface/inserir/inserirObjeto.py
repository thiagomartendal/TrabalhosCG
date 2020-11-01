from PyQt5.QtWidgets import *
from interface.inserir.montarPoligono import *
from interface.inserir.montarReta import *
from interface.inserir.montarPonto import *
from interface.inserir.montarSuperficie import *
from objeto.poligono import *
from objeto.linha import *
from objeto.ponto import *
from objeto.curva2D import *
from objeto.bSpline import *
from objeto.estruturaPonto import *
from objeto.ponto3D import *
from objeto.modeloArame import *
from objeto.segmentoReta import *
from objeto.superficieBicubica import *

class InserirObjeto(QDialog):
    __coordenadas = []  # Coordenadas para formar pontos do objeto
    __spfBezier = True  # superficie do tipo bezier

    # Construtor
    def __init__(self, tipo, parent=None):
        super(InserirObjeto, self).__init__()
        self.setWindowTitle("Inserir Objeto")
        self.setFixedSize(500, 230)
        self.__tipo = tipo
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.addWidget(self.__nomeForma())
        self.__sinalBotao = -1
        if self.__tipo == 0:
            mpol = MontarPoligono()
            self.__layout.addWidget(mpol)
            self.__coordenadas = mpol.coordenadas()
        elif self.__tipo == 1:
            mret = MontarReta();
            self.__layout.addWidget(mret)
            self.__coordenadas = mret.coordenadas()
        elif self.__tipo == 2:
            mpon = MontarPonto()
            self.__layout.addWidget(mpon)
            self.__coordenadas = mpon.coordenadas()
        elif self.__tipo == 3:
            mcur = MontarPoligono()
            self.__layout.addWidget(mcur)
            self.__coordenadas = mcur.coordenadas()
        elif self.__tipo == 4:
            mspl = MontarPoligono()
            self.__layout.addWidget(mspl)
            self.__coordenadas = mspl.coordenadas()
        elif self.__tipo == 5:
            self.setFixedSize(500, 250)
            mpol3D = MontarPoligono()
            self.__layout.addWidget(mpol3D)
            self.__layout.addWidget(QLabel("A cada 3 coordenadas tem-se um ponto."))
            self.__coordenadas = mpol3D.coordenadas()
        if self.__tipo != 6:
            self.__botoes(self.__layout)

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

    def __definirObjetos2D(self, nome, tmpC, multiPontos):
        if len(tmpC) % 2 != 0:
            QMessageBox.question(self, 'Atenção', 'Digite um número par de coordenadas para formar os pontos.', QMessageBox.Ok)
        else:
            pontos = []
            for i in range(0, len(tmpC)):
                if i % 2 != 0:
                    str1 = tmpC[i-1] if multiPontos else tmpC[i-1].text()
                    str2 = tmpC[i] if multiPontos else tmpC[i].text()
                    p = EstruturaPonto(float(str1), float(str2))
                    pontos.append(p)
                    i+1
            tmpC.clear()
            if self.__tipo == 0:
                self.__objeto = Poligono(nome, pontos)
            elif self.__tipo == 1:
                self.__objeto = Linha(nome, pontos)
            elif self.__tipo == 2:
                self.__objeto = Ponto(nome, pontos)
            elif self.__tipo == 3:
                self.__objeto = Curva2D(nome, pontos)
            elif self.__tipo == 4:
                self.__objeto = BSpline(nome, pontos)
            self.__sinalBotao = 0
            self.hide()

    def setSuperficieBezier(self, bezier):
        self.__spfBezier = bezier
        self.__inserirSuperficie()
        self.__botoes(self.__layout)

    def __inserirSuperficie(self):
        if self.__spfBezier:
            self.setFixedSize(500, 380)
        else:
            self.setFixedSize(500, 500)
        mspf3D = MontarSuperficie(self.__spfBezier)
        self.__layout.addWidget(mspf3D)
        self.__layout.addWidget(QLabel("A cada 3 coordenadas tem-se um ponto."))
        self.__coordenadas = mspf3D.coordenadas()
        self.__precisao = mspf3D.precisao()
        self.__tamanhoMatriz = mspf3D.tamanhoMatriz()

    def __definirObjetos3D(self, nome, tmpC, multiPontos):
        # pega os pontos do texto
        pontos = []
        for i in range(0, len(tmpC), 3):
            str1 = tmpC[i] if multiPontos else tmpC[i].text()
            str2 = tmpC[i+1] if multiPontos else tmpC[i+1].text()
            str3 = tmpC[i+2] if multiPontos else tmpC[i+2].text()
            pontos.append(Ponto3D(float(str1), float(str2), float(str3)))
        # para cada tipo de objeto
        if self.__tipo == 5:
            self.__objeto = ModeloArame(nome, pontos)
        elif self.__tipo == 6:
            if self.__spfBezier:
                tamanho = self.__tamanhoMatriz[0].text().split(' ')
                linhas  = int(tamanho[0]) if tamanho[0] else 4
                colunas = int(tamanho[1]) if tamanho[1] else 4
                if linhas < 4 or colunas < 4 or linhas > 20 or colunas > 20:
                    QMessageBox.question(self, 'Atenção', 'Tamanho de matriz invalida', QMessageBox.Ok)
                    return
                elif len(pontos) > linhas * colunas:
                    QMessageBox.question(self, 'Atenção', 'Mais pontos do que o tamanho da matriz', QMessageBox.Ok)
                    return
                elif len(pontos) < linhas * colunas:
                    QMessageBox.question(self, 'Atenção', 'Menos pontos do que o tamanho da matriz', QMessageBox.Ok)
                    return
            if len(pontos) < 16:
                QMessageBox.question(self, 'Atenção', 'São necessários 16 pontos para formar cada superfície.', QMessageBox.Ok)
                return
            else:
                precisao, deltaS, deltaT, tamanho = None, None, None, None
                if self.__spfBezier:
                    precisao = self.__precisao[0].text()
                    precisao = float(precisao) if precisao else None
                else:
                    deltaS  = self.__precisao[0].text()
                    deltaS  = float(deltaS) if deltaS else None
                    deltaT  = self.__precisao[1].text()
                    deltaT  = float(deltaT) if deltaT else None
                    tamanho = self.__tamanhoMatriz[0].text().split(' ')
                    linhas  = int(tamanho[0]) if tamanho[0] else 4
                    colunas = int(tamanho[1]) if tamanho[1] else 4
                    tamanho = [linhas, colunas]
                self.__objeto = SuperficieBicubica(nome, pontos, precisao, deltaS, deltaT, tamanho, self.__spfBezier)
        self.__sinalBotao = 0
        self.hide()

    # Ação do botão OK
    def __ok(self):
        nome = self.__nomeObjeto.text()
        multiPontos = self.__tipo == 0 or self.__tipo >= 3
        tmpC = []
        if multiPontos:
            if self.__tipo == 6:
                tmpC = self.__coordenadas[0].toPlainText()
            else:
                tmpC = self.__coordenadas[0].text()
            tmpC = tmpC.replace('\n', ' ')
            tmpC = tmpC.replace('  ', ' ')
            tmpC = tmpC.split(' ')
            if len(tmpC) < 2:
                QMessageBox.question(self, 'Atenção', 'São necessários mais pontos para criar um objeto.', QMessageBox.Ok)
                return
        else:
            tmpC = self.__coordenadas
        if self.__tipo >= 5:
            self.__definirObjetos3D(nome, tmpC, multiPontos)
        else:
            self.__definirObjetos2D(nome, tmpC, multiPontos)

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
