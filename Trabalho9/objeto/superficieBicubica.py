from numpy import transpose, matmul, array
from objeto.objeto3D import *
from objeto.ponto3D import *

class SuperficieBicubica(Objeto3D):
    # 0 0 0 0 30 40 0 60 30 0 100 0 30 25 20 20 60 50 30 80 50 40 0 20 60 30 20 80 60 50 70 100 45 60 0 25 100 0 0 110 30 40 110 60 30 100 90 0

    def __init__(self, nome, pontosControle, precisao=None, bezier=True):
        self.__pontosControle = pontosControle
        self.__precisao = precisao if precisao else 0.1
        segmentos  = self.calcularSegmentos(pontosControle, self.__precisao, bezier)
        super(SuperficieBicubica, self).__init__(nome, segmentos)

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 6

    # Retorna os pontos de controle
    def getPontosControle(self):
        return self.__pontosControle

    # Retorna a precisao do delta
    def getPrecisao(self):
        return self.__precisao

    # Retorna uma lista de segmentos da superficie com base na precisao
    def calcularSegmentos(self, pontosControle, delta, bezier):
        segmentos = []
        M = self.transformacaoBezier() if bezier else self.transformacaoSpline()
        MT = transpose(M)
        # Calcula a superficie a cada 16 pontos
        for k in range(len(pontosControle)//16):
            pontos = pontosControle[k*16: (k+1)*16]
            Gx = [ [p.X() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            Gy = [ [p.Y() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            Gz = [ [p.Z() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            #
            for s in range(int(1/delta)):
                s = float(delta * s)
                S = [s**3, s**2, s, 1]
                #
                pontosCurva = []
                for t in range(int(1/delta)):
                    t = float(delta * t)
                    TT = transpose([t**3, t**2, t, 1])
                    #
                    x = matmul(S, matmul(M, matmul(Gx, matmul(MT, TT) )))
                    y = matmul(S, matmul(M, matmul(Gy, matmul(MT, TT) )))
                    z = matmul(S, matmul(M, matmul(Gz, matmul(MT, TT) )))
                    pontosCurva.append(Ponto3D(x,y,z))
                # crio a curva
                prev = pontosCurva.pop(0)
                for p in pontosCurva:
                    segmentos.append(SegmentoReta(prev, p))
                    prev = p
        return segmentos

    # Realiza a transformação com a matriz de bézier
    def transformacaoBezier(self):
        MB = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        return MB

    # Realiza a transformação com a matriz de b-spline
    def transformacaoSpline(self):
        M = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        Mbs = (1/6)*M
        return Mbs
