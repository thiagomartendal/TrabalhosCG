from PyQt5.QtWidgets import *

class MontarSuperficie(QFrame):

    # Construtor
    def __init__(self, parent=None):
        super(MontarSuperficie, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Coordenadas"))

        input = QTextEdit()
        input.setMinimumSize(input.width(), 80)
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

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas

    # Precisao do delta
    def precisao(self):
        return self.__precisao
