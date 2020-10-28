from numpy import transpose, matmul, array
from objeto.objeto3D import *
from objeto.ponto3D import *

class SuperficieBicubica(Objeto3D):
    # 0 0 0 0 30 40 0 60 30 0 100 0 30 25 20 20 60 50 30 80 50 40 0 20 60 30 20 80 60 50 70 100 45 60 0 25 100 0 0 110 30 40 110 60 30 100 90 0
    # -250 -300 0 -250 -150 200 -250 0 150 -250 200 0 -100 -175 100 -150 0 250 -100 100 250 -50 -300 100 50 -150 100 150 0 250 100 200 225 50 -300 125 250 -300 0 300 -150 200 300 0 150 250 150 0

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
        if bezier:
            return self.__calcBezier(pontosControle, delta)
        else:
            return self.__calcSpline(pontosControle, delta, delta)

    # Retorna uma lista de segmentos da superficie bicubica de bezier com base na precisao
    def __calcBezier(self, pontosControle, delta):
        segmentos = []
        M = self.__transformacaoBezier()
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
                    x = self.__multmat([S, M, Gx, MT, TT])
                    y = self.__multmat([S, M, Gy, MT, TT])
                    z = self.__multmat([S, M, Gz, MT, TT])
                    pontosCurva.append(Ponto3D(x,y,z))
                # crio a curva
                prev = pontosCurva.pop(0)
                for p in pontosCurva:
                    segmentos.append(SegmentoReta(prev, p))
                    prev = p
        return segmentos

    # Retorna uma lista de segmentos da superficie bicubica Spline com base na precisao
    def __calcSpline(self, pontosControle, deltaS, deltaT):
        segmentos = []
        M = self.__transformacaoSpline()
        MT = transpose(M)
        for k in range(len(pontosControle)//16):
            pontos = pontosControle[k*16: (k+1)*16]
            Gx = [ [p.X() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            Gy = [ [p.Y() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            Gz = [ [p.Z() for p in pontos][i: i+4] for i in range(0, 16, 4) ]
            #
            Cx = self.__multmat([M, Gx, MT])
            Cy = self.__multmat([M, Gy, MT])
            Cz = self.__multmat([M, Gz, MT])
            # crio as matrizes E
            ns = int(1/deltaS)
            nt = int(1/deltaT)
            Eds = self.__matE(deltaS)
            EdtT = transpose(self.__matE(deltaT))
            # calculo as fwdDiffs
            segmentos += self.__superficieFwdDiff(ns, nt, Cx, Cy, Cz, Eds, EdtT)
        return segmentos

    # Retorna lista de segmentos da superficie de 16 pontos
    def __superficieFwdDiff(self, ns, nt, Cx, Cy, Cz, Eds, EdtT):
        segmentos = []
        # crio as matrizes
        DDx = self.__multmat([Eds, Cx, EdtT])
        DDy = self.__multmat([Eds, Cy, EdtT])
        DDz = self.__multmat([Eds, Cz, EdtT])
        # ns curvas ao longo de t
        for _ in range(ns+1):
            x,y,z = self.__curvaFwdDiff(nt, DDx[0], DDy[0], DDz[0])
            DDx = self.__atualizarDD(DDx)
            DDy = self.__atualizarDD(DDy)
            DDz = self.__atualizarDD(DDz)
            # add ponto
            prev = None
            for _ in range(len(x)):
                ponto = Ponto3D(x.pop(0), y.pop(0), z.pop(0))
                if prev:
                    segmentos.append(SegmentoReta(prev, ponto))
                prev = ponto
        # re-crio as matrizes
        DDx = self.__multmat([Eds, Cx, EdtT])
        DDy = self.__multmat([Eds, Cy, EdtT])
        DDz = self.__multmat([Eds, Cz, EdtT])
        # transpostas
        DDx = transpose(DDx)
        DDy = transpose(DDy)
        DDz = transpose(DDz)
        # nt curvas ao longo de s
        for _ in range(nt+1):
            x,y,z = self.__curvaFwdDiff(ns, DDx[0], DDy[0], DDz[0])
            DDx = self.__atualizarDD(DDx)
            DDy = self.__atualizarDD(DDy)
            DDz = self.__atualizarDD(DDz)
            # add ponto
            prev = None
            for _ in range(len(x)):
                ponto = Ponto3D(x.pop(0), y.pop(0), z.pop(0))
                if prev:
                    segmentos.append(SegmentoReta(prev, ponto))
                prev = ponto
        return segmentos

    # Calcula as FwdDiff para uma curva
    def __curvaFwdDiff(self, n, DDxr, DDyr, DDzr):
        x, dx, d2x, d3x = DDxr
        y, dy, d2y, d3y = DDyr
        z, dz, d2z, d3z = DDzr
        xs = [float(x)]
        ys = [float(y)]
        zs = [float(z)]
        i = 0
        while i < n:
            i += 1
            # X
            x = x + dx
            dx = dx+ d2x
            d2x = d2x+ d3x
            # Y
            y = y + dy
            dy = dy+ d2y
            d2y = d2y+ d3y
            # Z
            z = z + dz
            dz = dz+ d2z
            d2z = d2z+ d3z
            # adiciona na lista
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
        return xs, ys, zs

    # Retorna a matriz de bézier
    def __transformacaoBezier(self):
        MB = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        return MB

    # Retorna a matriz de b-spline
    def __transformacaoSpline(self):
        M = array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        Mbs = (1/6)*M
        return Mbs

    # Retorna a matriz e com base no delta 'd'
    def __matE(self, d):
        return [[0,0,0,1], [d**3,d**2,d,0], [6*d**3,2*d**2,0,0],[6*d**3,0,0,0]]

    # Retorna a matriz DD atualizada
    def __atualizarDD(self, DD):
        return [
                (DD[0]+DD[1]),
                (DD[1]+DD[2]),
                (DD[2]+DD[3]),
                DD[3]
                ]

    # Retorna a matriz resultante da multiplicacao de uma lista de matrizes
    def __multmat(self, matrizes):
        result = matrizes.pop(-1)
        for _ in range(len(matrizes)):
            m = matrizes.pop(-1)
            result = matmul(m, result)
        return result