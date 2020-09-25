from PyQt5.QtWidgets import *

class MontarPonto(QFrame):

    # Construtor
    def __init__(self, parent=None):
        super(MontarPonto, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        layoutPainel1 = QHBoxLayout()
        painel1 = QFrame()
        painel1.setLayout(layoutPainel1)
        layoutPainel.addWidget(QLabel("Coordenadas"))
        x = QLineEdit()
        y = QLineEdit()
        layoutPainel1.addWidget(QLabel("X: "))
        layoutPainel1.addWidget(x)
        layoutPainel1.addWidget(QLabel("Y: "))
        layoutPainel1.addWidget(y)
        layoutPainel.addWidget(painel1)
        self.__coordenadas = [x, y]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas
