from PyQt5.QtWidgets import *

class MontarReta(QFrame):

    # Construtor
    def __init__(self, parent=None):
        super(MontarReta, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        layoutPainel1 = QHBoxLayout()
        painel1 = QFrame()
        painel1.setLayout(layoutPainel1)
        layoutPainel.addWidget(QLabel("Coordenadas"))
        x1 = QLineEdit()
        y1 = QLineEdit()
        x2 = QLineEdit()
        y2 = QLineEdit()
        layoutPainel1.addWidget(QLabel("X1: "))
        layoutPainel1.addWidget(x1)
        layoutPainel1.addWidget(QLabel("Y1: "))
        layoutPainel1.addWidget(y1)
        layoutPainel1.addWidget(QLabel("X2: "))
        layoutPainel1.addWidget(x2)
        layoutPainel1.addWidget(QLabel("Y2: "))
        layoutPainel1.addWidget(y2)
        layoutPainel.addWidget(painel1)
        self.__coordenadas = [x1, y1, x2, y2]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas
