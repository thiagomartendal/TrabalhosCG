from PyQt5.QtWidgets import *

class MontarPoligono(QFrame):

    # Construtor
    def __init__(self, parent=None):
        super(MontarPoligono, self).__init__()
        layoutPainel = QVBoxLayout()
        self.setLayout(layoutPainel)
        layoutPainel.addWidget(QLabel("Coordenadas"))
        input = QLineEdit()
        layoutPainel.addWidget(input)
        layoutPainel.addWidget(QLabel("Separe cada coordenada com espaços."))
        self.__coordenadas = [input]

    # Coordenadas fornecidas
    def coordenadas(self):
        return self.__coordenadas
