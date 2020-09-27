from objeto.objeto import *
from objeto.estruturaPonto import *

class Clipping:

    # Construtor
    def __init__(self, viewportCoordenadas):
        self.__xEsq = viewportCoordenadas[0]
        self.__yTop = viewportCoordenadas[1]
        self.__xDir = viewportCoordenadas[2]
        self.__yBot = viewportCoordenadas[3]

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
            if novos != []:
                objeto.setPontos(novos)
            else:
                objeto.clearPontos()
        # curva
        elif objeto.tipo() == 3:
            novos = self.__clippingCurva(pontos)
            if novos != []:
                objeto.setPontos(novos)
            else:
                objeto.clearPontos()
        # poligono
        elif len(pontos) > 2:
            novos = self.__clippingSutherlandHodgeman(pontos)
            if novos != []:
                objeto.setPontos(novos)
            else:
                objeto.clearPontos()

    # Boolean para ponto esta dentro da window
    def __dentroWindow(self, p):
        if p.X() > self.__xDir or p.X() < self.__xEsq:  return False
        if p.Y() < self.__yTop or p.Y() > self.__yBot:  return False
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
            return []            # novos = pontos
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
                        pontos[i1] = self.__direita(pontos[i1], pontos[i2])
                    if pos[1]:         # 0010 esquerda da window
                        pontos[i1] = self.__esquerda(pontos[i1], pontos[i2])
                    if pos[2]:         # 0100 em cima da window
                        pontos[i1] = self.__topo(pontos[i1], pontos[i2])
                    if pos[0]:         # 0001 em baixo da window
                        pontos[i1] = self.__fundo(pontos[i1], pontos[i2])
                    pos = self.__posicao(pontos[i1])
                if sum(pos) != 0:
                    return []
            return pontos

    # Clipping de poligo Sutherland-Hodgeman
    def __clippingSutherlandHodgeman(self, pontos):
        # eixo X
        novosPontosEixoX = []
        for i in range(len(pontos)):
            p1 = pontos[i]
            p2 = pontos[(i+1)%len(pontos)]
            # adiciono os pontos dentro dos limites esq e dir, mas que podem estar fora dos limites de Y da window
            if p1.X() <= self.__xDir and p1.X() >= self.__xEsq and p2.X() <= self.__xDir and p2.X() >= self.__xEsq:
                novosPontosEixoX.append(p1)
            # p1 dentro e p2 fora pela direita da window
            elif p1.X() < self.__xDir and p2.X() > self.__xDir:
                novosPontosEixoX.append(p1)
                novosPontosEixoX.append(self.__direita(p1, p2))
            # p1 dentro e p2 fora pela esquerda da window
            elif p1.X() > self.__xEsq and p2.X() < self.__xEsq:
                novosPontosEixoX.append(p1)
                novosPontosEixoX.append(self.__esquerda(p1, p2))
            # p2 dentro e p1 fora pela direita da window
            elif p2.X() < self.__xDir and p1.X() > self.__xDir:
                novosPontosEixoX.append(self.__direita(p2, p1))
            # p2 dentro e p1 fora pela esquerda da window
            elif p2.X() > self.__xEsq and p1.X() < self.__xEsq:
                novosPontosEixoX.append(self.__esquerda(p2, p1))
        # eixo Y
        novosPontosEixoXY = []
        for i in range(len(novosPontosEixoX)):
            p1 = novosPontosEixoX[i]
            p2 = novosPontosEixoX[(i+1)%len(novosPontosEixoX)]
            # ambos dentro
            if self.__dentroWindow(p1) and self.__dentroWindow(p2):
                novosPontosEixoXY.append(p1)
            # p1 dentro e p2 fora pelo topo da window
            elif p1.Y() > self.__yTop and p2.Y() < self.__yTop:
                novosPontosEixoXY.append(p1)
                novosPontosEixoXY.append(self.__topo(p1, p2))
            # p1 dentro e p2 fora pelo fundo da window
            elif p1.Y() < self.__yBot and p2.Y() > self.__yBot:
                novosPontosEixoXY.append(p1)
                novosPontosEixoXY.append(self.__fundo(p1, p2))
            # p2 dentro e p1 fora pelo topo da window
            elif p2.Y() > self.__yTop and p1.Y() < self.__yTop:
                novosPontosEixoXY.append(self.__topo(p2, p1))
            # p2 dentro e p1 fora pelo fundo da window
            elif p2.Y() < self.__yBot and p1.Y() > self.__yBot:
                novosPontosEixoXY.append(self.__fundo(p2, p1))
        return novosPontosEixoXY

    # Clipping de Curva2D
    def __clippingCurva(self, pontos):
        novosPontos = []
        for i in range(len(pontos)-1):
            p1 = pontos[i]
            p2 = pontos[i+1]
            if self.__dentroWindow(p1) and self.__dentroWindow(p2):
                novosPontos.append(p1)
            elif self.__dentroWindow(p1) or self.__dentroWindow(p2):
                novosPontos += self.__clippingCohenSutherland(p1, p2)
            else:
                novosPontos.append(-1)
        return novosPontos

    # Vetor com a posicao do ponto em relacao a window
    def __posicao(self, p):
        posicao = [False for _ in range(4)]
        if p.X() > self.__xDir:     posicao[3] = True   # 1000 direita da window
        elif p.X() < self.__xEsq:   posicao[1] = True   # 0010 esquerda da window
        if p.Y() < self.__yTop:    posicao[2] = True   # 0100 em cima da window
        elif p.Y() > self.__yBot: posicao[0] = True   # 0001 em baixo da window
        return posicao

    # Retorna o ponto para coincidir com o canto direito da window
    def __direita(self, p1, p2):
        m = self.__coefAngular(p1, p2)
        y = m * (self.__xDir - p1.X()) + p1.Y()
        return EstruturaPonto(self.__xDir, y)

    # Retorna o ponto para coincidir com o canto esquerdo da window
    def __esquerda(self, p1, p2):
        m = self.__coefAngular(p1, p2)
        y = m * (self.__xEsq - p1.X()) + p1.Y()
        return EstruturaPonto(self.__xEsq, y)

    # Retorna o ponto para coincidir com o canto em cima da window
    def __topo(self, p1, p2):
        umSobreM = self.__inversoCoefAngular(p1, p2)
        x = p1.X() + umSobreM * (self.__yTop - p1.Y())
        return EstruturaPonto(x, self.__yTop)

    # Retorna o ponto para coincidir com o canto em baixo da window
    def __fundo(self, p1, p2):
        umSobreM = self.__inversoCoefAngular(p1, p2)
        x = p1.X() + umSobreM * (self.__yBot - p1.Y())
        return EstruturaPonto(x, self.__yBot)

    # Retorna o coeficiente angular da reta
    def __coefAngular(self, p1, p2):
        return (p2.Y() - p1.Y()) / (p2.X() - p1.X())

    # Retorna 1 / coeficiente angular da reta
    def __inversoCoefAngular(self, p1, p2):
        return (p2.X() - p1.X()) / (p2.Y() - p1.Y())
