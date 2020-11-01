from PyQt5.QtWidgets import *

class MontarSuperficie(QFrame):

    # Construtor
    def __init__(self, bezier, parent=None):
        super(MontarSuperficie, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Coordenadas"))

        input = QTextEdit()
        input.setText("-250 -300 0 -250 -150 200 -250 0 150 -250 200 0 -100 -175 100 -150 0 250 -100 100 250 -50 -300 100 50 -150 100 150 0 250 100 200 225 50 -300 125 250 -300 0 300 -150 200 300 0 150 250 150 0")
        input.setMinimumSize(400, 80)
        layoutPainel.addWidget(input)
        layoutPainel.addWidget(QLabel("Separe cada coordenada com espaços."))
        self.__coordenadas = [input]

        # painel precisao
        layoutPainelPrec = QHBoxLayout()
        painelPrec = QFrame()
        painelPrec.setLayout(layoutPainelPrec)
        painelPrec.setMaximumWidth(self.width()*(0.3))
        # caixas de texto da precisao
        precisao = QLineEdit()
        precisao.setText('0.1')
        if bezier:
            layoutPainelPrec.addWidget(QLabel("Precisao (entre 0 e 1)"))
        else:
            painelPrec.setMaximumWidth(self.width()*(0.5))
            precisao2 = QLineEdit()
            precisao2.setText('0.1')
            layoutPainelPrec.addWidget(QLabel("DeltaS DeltaT (entre 0 e 1)"))
        # add ao painel
        layoutPainelPrec.addWidget(precisao)
        self.__precisao = [precisao]
        if not bezier:
            layoutPainelPrec.addWidget(precisao2)
            self.__precisao += [precisao2]
        layoutPainel.addWidget(painelPrec)
        # tamanho da matriz
        self.__tamanhoMatriz = None
        if not bezier:
            layoutPainelMat = QHBoxLayout()
            painelMat = QFrame()
            painelMat.setLayout(layoutPainelMat)
            painelMat.setMaximumWidth(self.width()*(0.4))
            layoutPainelMat.addWidget(QLabel("Linhas Colunas (4 4 até 20 20)"))
            tamanhoMatriz = QLineEdit()
            tamanhoMatriz.setText('4 4')
            layoutPainelMat.addWidget(tamanhoMatriz)
            layoutPainel.addWidget(painelMat)
            layoutPainel.addWidget(QLabel("Preencha as coordenadas faltantes com 1's para ocupar as dimensões da matriz."))
            self.__tamanhoMatriz = [tamanhoMatriz]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas

    # Precisao do delta
    def precisao(self):
        return self.__precisao

    def tamanhoMatriz(self):
        return self.__tamanhoMatriz
