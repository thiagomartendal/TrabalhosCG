from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.ponto3D import *
from objeto.segmentoReta import *
from objeto.objeto3D import *
from numpy import matmul
from math import sin, cos, radians, acos, degrees

class ModeloArame(Objeto3D):
# 0 0 0 100 0 0 100 100 0 0 100 0
# 0 0 0 100 0 0 100 0 100 0 0 100 0 100 100 0 100 0 0 0 0 0 0 100 0 100 100 100 100 100 100 0 100 100 100 100 100 100 0 100 0 0 100 100 0 0 100 0
# 0 0 0 100 0 0 100 0 100 0 0 100 0 100 100 0 100 0 0 0 0 0 0 100 0 100 100 100 100 100 100 0 100 100 100 100 100 100 0 100 0 0 100 100 0 0 100 0 0 0 0 50 50 50

    # Construtor
    def __init__(self, nome, pontos):
        super(ModeloArame, self).__init__(nome, self.paraSegmentos(pontos))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 5

