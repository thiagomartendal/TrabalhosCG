from numpy import *
from objeto.objeto3D import *

class SuperficieBicubica(Objeto3D):

    def __init__(self, nome, pontos3D):
        super(SuperficieBicubica, self).__init__(nome, pontos3D)

    # Desenha o objeto
    def desenhar(self, cena):
        pass

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 6

    # Define as matrizes de coeficientes
    def __definirMatrizesG(self):
        self.__Gx = []
        self.__Gy = []
        self.__Gz = []
        lx = []
        ly = []
        lz = []
        k = 1
        for i in range(0, len(self.getPontos())):
            lx.append(self.getPontos()[i].X())
            ly.append(self.getPontos()[i].Y())
            lz.append(self.getPontos()[i].Z())
            k += 1
            if k == 4:
                self.__Gx.append(lx)
                self.__Gy.append(ly)
                self.__Gz.append(lz)
                lx.clear()
                ly.clear()
                lz.clear()
                k = 1

    # Método para transformação de superfície bicúbica
    def __transformar(self, M):
        self.__definirMatrizesG()
        MT = M.transpose()
        s = 0.0
        t = 0.0
        for s in range(0, 10, 1):
            S = array([(s/10)**3, (s/10)**2, (s/10), 1])
            for t in range(0, 10, 1):
                T = array([(t/10)**3, (t/10)**2, t/10, 1])
                TT = T.transpose()
                x = matmul(S, matmul(M, matmul(self.__Gx, matmul(MT, TT))))
                y = matmul(S, matmul(M, matmul(self.__Gy, matmul(MT, TT))))
                z = matmul(S, matmul(M, matmul(self.__Gz, matmul(MT, TT))))

    # Realiza a transformação com a matriz de bézier
    def transformacaoBezier(self):
        MB = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        self.__transformar(MB)

    # Realiza a transformação com a matriz de b-spline
    def transformacaoSpline(self):
        M = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        Mbs = (1/6)*M
        self.__transformar(Mbs)
