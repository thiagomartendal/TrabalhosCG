from PyQt5.QtWidgets import *

class MontarSuperficie(QFrame):

    # Construtor
    def __init__(self, caixasDelta, parent=None):
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
        precisao = QLineEdit()
        precisao.setText('0.1')
        layoutPainelPrec.addWidget(QLabel("Precisao (entre 0 e 1)"))
        layoutPainelPrec.addWidget(precisao)
        self.__precisao = [precisao]
        layoutPainel.addWidget(painelPrec)

        if caixasDelta:
            layoutDeltaS = QHBoxLayout()
            painelDeltaS = QFrame()
            deltaS = QLineEdit()
            layoutDeltaS.addWidget(QLabel("Delta S: "))
            layoutDeltaS.addWidget(deltaS)
            painelDeltaS.setLayout(layoutDeltaS)
            layoutDeltaT = QHBoxLayout()
            painelDeltaT = QFrame()
            deltaT = QLineEdit()
            layoutDeltaT.addWidget(QLabel("Delta T: "))
            layoutDeltaT.addWidget(deltaT)
            painelDeltaT.setLayout(layoutDeltaT)
            layoutPainel.addWidget(painelDeltaS)
            layoutPainel.addWidget(painelDeltaT)
            self.__deltaS = [deltaS]
            self.__deltaT = [deltaT]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas

    # Precisao do delta
    def precisao(self):
        return self.__precisao

    # DeltaS
    def deltaS(self):
        return self.__deltaS

    # DeltaT
    def deltaT(self):
        return self.__deltaT
