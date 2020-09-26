from PyQt5.QtWidgets import *

class MontarCurva(QFrame):

    # Construtor
    def __init__(self, parent=None):
        super(MontarCurva, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        self.__coordenadas = []
        layoutPainel.addWidget(QLabel("Ponto 1 (Linha)"))
        layoutPainel1 = QHBoxLayout()
        painel1 = QFrame()
        painel1.setLayout(layoutPainel1)
        self.__coordenadas.append(self.__coord(layoutPainel1))
        layoutPainel.addWidget(painel1)
        layoutPainel.addWidget(QLabel("Ponto 2 (Guia da Curva)"))
        layoutPainel2 = QHBoxLayout()
        painel2 = QFrame()
        painel2.setLayout(layoutPainel2)
        self.__coordenadas.append(self.__coord(layoutPainel2))
        layoutPainel.addWidget(painel2)
        layoutPainel.addWidget(QLabel("Ponto 3 (Guia da Curva)"))
        layoutPainel3 = QHBoxLayout()
        painel3 = QFrame()
        painel3.setLayout(layoutPainel3)
        self.__coordenadas.append(self.__coord(layoutPainel3))
        layoutPainel.addWidget(painel3)
        layoutPainel.addWidget(QLabel("Ponto 4 (Linha)"))
        layoutPainel4 = QHBoxLayout()
        painel4 = QFrame()
        painel4.setLayout(layoutPainel4)
        self.__coordenadas.append(self.__coord(layoutPainel4))
        layoutPainel.addWidget(painel4)

    def __coord(self, layout):
        x = QLineEdit()
        y = QLineEdit()
        layout.addWidget(QLabel("X: "))
        layout.addWidget(x)
        layout.addWidget(QLabel("Y: "))
        layout.addWidget(y)
        return [x, y]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas
