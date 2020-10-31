from numpy import transpose, matmul, array
from objeto.objeto3D import *
from objeto.ponto3D import *

class SuperficieBicubica(Objeto3D):
    # 0 0 0 0 30 40 0 60 30 0 100 0 30 25 20 20 60 50 30 80 50 40 0 20 60 30 20 80 60 50 70 100 45 60 0 25 100 0 0 110 30 40 110 60 30 100 90 0
    # -250 -300 0 -250 -150 200 -250 0 150 -250 200 0 -100 -175 100 -150 0 250 -100 100 250 -50 -300 100 50 -150 100 150 0 250 100 200 225 50 -300 125 250 -300 0 300 -150 200 300 0 150 250 150 0

    def __init__(self, nome, pontosControle, precisao=None, deltaS=None, deltaT=None, bezier=True):
        self.__pontosControle = pontosControle
        self.__precisao = precisao if precisao else 0.1
        self.__deltaS = deltaS if deltaS else 0.1
        self.__deltaT = deltaT if deltaT else 0.1
        segmentos  = self.calcularSegmentos(pontosControle, bezier)
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
    def calcularSegmentos(self, pontosControle, bezier):
        if bezier:
            return self.__calcBezier(pontosControle, self.__precisao)
        else:
            return self.__calcSpline(pontosControle, self.__deltaS, self.__deltaT)

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

    # Define a dimensão da matriz
    def __definirDimensao(self, qtdPontos):
        if qtdPontos >= 1 and qtdPontos <= 16:
            return 4
        elif qtdPontos >= 17 and qtdPontos <= 25:
            return 5
        elif qtdPontos >= 26 and qtdPontos <= 36:
            return 6
        elif qtdPontos >= 37 and qtdPontos <= 49:
            return 7
        elif qtdPontos >= 50 and qtdPontos <= 64:
            return 8
        elif qtdPontos >= 65 and qtdPontos <= 81:
            return 9
        elif qtdPontos >= 82 and qtdPontos <= 100:
            return 10
        elif qtdPontos >= 101 and qtdPontos <= 121:
            return 11
        elif qtdPontos >= 122 and qtdPontos <= 144:
            return 12
        elif qtdPontos >= 145 and qtdPontos <= 169:
            return 13
        elif qtdPontos >= 170 and qtdPontos <= 196:
            return 14
        elif qtdPontos >= 197 and qtdPontos <= 225:
            return 15
        elif qtdPontos >= 226 and qtdPontos <= 256:
            return 16
        elif qtdPontos >= 257 and qtdPontos <= 289:
            return 17
        elif qtdPontos >= 290 and qtdPontos <= 324:
            return 18
        elif qtdPontos >= 325 and qtdPontos <= 361:
            return 19
        elif qtdPontos >= 362 and qtdPontos <= 400:
            return 20
        return -1

    # Monta os coeficientes nas matrizes
    def __montarMatrizes(self, pontos):
        n = self.__definirDimensao(len(pontos))
        Gx = [[1 for x in range(n)] for y in range(n)]
        Gy = [[1 for x in range(n)] for y in range(n)]
        Gz = [[1 for x in range(n)] for y in range(n)]
        k = 0
        for i in range(n):
            for j in range(n):
                if k < len(pontos):
                    Gx[i][j] = pontos[k].X()
                    Gy[i][j] = pontos[k].Y()
                    Gz[i][j] = pontos[k].Z()
                    k += 1
        return Gx, Gy, Gz

    # Retorna uma lista de segmentos da superficie bicubica Spline com base na precisao
    def __calcSpline(self, pontosControle, deltaS, deltaT):
        x, y, z = self.__montarMatrizes(pontosControle)
        print('Gx:', x)
        print('Gy:', y)
        print('Gz:', z)
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
