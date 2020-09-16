from objeto.objeto import *
from objeto.estruturaPonto import *

class Clipping:

    # Construtor
    def __init__(self, viewportCoordenadas):
        self.__xEsq = viewportCoordenadas[0]
        self.__yFundo = viewportCoordenadas[1]
        self.__xDir = viewportCoordenadas[2]
        self.__yTopo = viewportCoordenadas[3]

    # Clipping
    def clip(self, objeto):
        pontos = objeto.getPontos()
        # ponto
        if len(pontos) == 1:
            if not self.__dentroWindow(pontos[0]):
                objeto.clearPontos()
        # linha
        elif len(pontos) == 2:
            p1 = pontos[0]
            p2 = pontos[1]
            novos = self.__clippingCohenSutherland(p1, p2)
            if novos != None: 
                objeto.setPontos(novos)
            else:
                objeto.clearPontos()
        # poligono
        elif len(pontos) > 2:
            pass

    # Boolean para ponto esta dentro da window
    def __dentroWindow(self, p):
        if p.X() > self.__xDir or p.X() < self.__xEsq:      return False
        if p.Y() > self.__yTopo or p.Y() < self.__yFundo:   return False
        return True

    # Clipping de reta Cohen-Sutherland
    def __clippingCohenSutherland(self, p1, p2):
        pos1 = self.__posicao(p1)
        pos2 = self.__posicao(p2)
        # ambos dentro
        if pos1 == pos2 and sum(pos1) == 0:
            return [p1, p2]
        # mesma zona (esq, dir, topo, fundo) 
        elif sum([pos1[i] and pos2[i] for i in range(4)]) != 0:
            return None
        # cortar a reta
        else:
            pontos = [p1, p2]
            for i1 in range(2):
                i2 = (i1+1)%2
                pos = self.__posicao(pontos[i1])
                # caso corte com o lado de fora de um dos eixos, corte novamente
                cortar = sum(pos)
                for _ in range(cortar):
                    if pos[3]:         # 1000 direita da window
                        self.__direita(pontos[i1], pontos[i2])
                    if pos[1]:         # 0010 esquerda da window
                        self.__esquerda(pontos[i1], pontos[i2])
                    if pos[2]:         # 0100 em cima da window
                        self.__topo(pontos[i1], pontos[i2])
                    if pos[0]:         # 0001 em baixo da window
                        self.__fundo(pontos[i1], pontos[i2])
                    pos = self.__posicao(pontos[i1])
                if sum(pos) != 0:
                    return None
            return pontos

    # Vetor com a posicao do ponto em relacao a window
    def __posicao(self, p):
        posicao = [False for _ in range(4)]
        if p.X() > self.__xDir:     posicao[3] = True   # 1000 direita da window
        elif p.X() < self.__xEsq:   posicao[1] = True   # 0010 esquerda da window
        if p.Y() > self.__yTopo:    posicao[2] = True   # 0100 em cima da window
        elif p.Y() < self.__yFundo: posicao[0] = True   # 0001 em baixo da window
        return posicao
    
    # Modifica o ponto para coincidir com o canto direito da window
    def __direita(self, p1, p2):
        m = (p2.Y() - p1.Y()) / (p2.X() - p1.X())
        y = m * (self.__xDir - p1.X()) + p1.Y()
        p1.setX(self.__xDir)
        p1.setY(y)
        
    # Modifica o ponto para coincidir com o canto esquerdo da window
    def __esquerda(self, p1, p2):
        m = (p2.Y() - p1.Y()) / (p2.X() - p1.X())
        y = m * (self.__xEsq - p1.X()) + p1.Y()
        p1.setX(self.__xEsq)
        p1.setY(y)
        
    # Modifica o ponto para coincidir com o canto em cima da window
    def __topo(self, p1, p2):
        umSobreM = (p2.X() - p1.X()) / (p2.Y() - p1.Y())
        x = p1.X() + umSobreM * (self.__yTopo - p1.Y())
        p1.setX(x)
        p1.setY(self.__yTopo)
        
    # Modifica o ponto para coincidir com o canto em baixo da window
    def __fundo(self, p1, p2):
        umSobreM = (p2.X() - p1.X()) / (p2.Y() - p1.Y())
        x = p1.X() + umSobreM * (self.__yFundo - p1.Y())
        p1.setX(x)
        p1.setY(self.__yFundo)
