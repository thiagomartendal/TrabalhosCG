from objeto.objeto import *
from objeto.estruturaPonto import *

class Clipping:

    # Construtor
    def __init__(self, viewportCoordenadas):
        self.__xEsq = viewportCoordenadas[0]
        self.__yTop = viewportCoordenadas[1]
        self.__xDir = viewportCoordenadas[2]
        self.__yBot = viewportCoordenadas[3]
        self.__pontosViewport = [EstruturaPonto(viewportCoordenadas[0], viewportCoordenadas[1]),    # esq top
                                 EstruturaPonto(viewportCoordenadas[0], viewportCoordenadas[3]),    # esq bot
                                 EstruturaPonto(viewportCoordenadas[2], viewportCoordenadas[1]),    # dir top
                                 EstruturaPonto(viewportCoordenadas[2], viewportCoordenadas[3])]    # dir bot

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
            # fora da window
            if not (self.__dentroWindow(p1) and self.__dentroWindow(p2)):
                novos = self.__clippingCohenSutherland(p1, p2)
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

    # Nicholl-Lee-Nicholl
    def __clippingNichollLeeNicholl(self, p1, p2):
        # uso p1 como o ponto mais a esq
        if p1.X() > p2.X():
            t = p1
            p1 = p2
            p2 = t
        mr = self.__coefAngular(p1, p2)
        m1 = self.__coefAngular(p1, self.__pontosViewport[0]) # esq top
        m2 = self.__coefAngular(p1, self.__pontosViewport[2]) # dir top
        m3 = self.__coefAngular(p1, self.__pontosViewport[3]) # dir bot
        m4 = self.__coefAngular(p1, self.__pontosViewport[1]) # esq bot
        if self.__dentroWindow(p1):
            if   m1 < mr and mr < m4:   # esq
                novo = self.__esquerda(p1, p2)
                return [p1, novo]
            elif m1 < mr and mr < m2:   # top
                novo = self.__topo(p1, p2)
                return [p1, novo]
            elif m2 < mr and mr < m3:   # dir
                novo = self.__direita(p1, p2)
                return [p1, novo]
            elif m3 < mr and mr < m4:   # bot
                novo = self.__fundo(p1, p2)
                return [p1, novo]
        else:
            if m4 < mr and mr < m1:
                return []
            # esq da window
            if p1.X() < self.__xEsq:
                if   m1 < mr and mr < m2:
                    novo1 = self.__esquerda(p1, p2)
                    novo2 = self.__topo(p1, p2) if p2.Y() < self.__yTop else p2
                    return [novo1, novo2]
                elif m2 < mr and mr < m3:
                    novo1 = self.__esquerda(p1, p2)
                    novo2 = self.__direita(p1, p2) if p2.X() > self.__xDir else p2
                    return [novo1, novo2]
                elif m3 < mr and mr < m4:
                    novo1 = self.__esquerda(p1, p2)
                    novo2 = self.__fundo(p1, p2) if p2.Y() > self.__yBot else p2
                    return [novo1, novo2]
            # esq cima
            if p1.Y() < self.__yBot:
                if   m1 < mr and mr < m2:
                    novo1 = self.__topo(p1, p2)
                    novo2 = self.__esquerda(p1, p2) if p2.X() > self.__xDir else p2
                    return [novo1, novo2]
                elif m3 < mr and mr < m4:
                    novo1 = self.__esquerda(p1, p2)
                    novo2 = self.__fundo(p1, p2) if p2.Y() > self.__yBot else p2
                    return [novo1, novo2]
                elif m2 < mr and mr < m3:
                    novo1 = self.__topo(p1, p2)
                    novo2 = self.__fundo(p1, p2) if p2.Y() > self.__yBot else p2
                    return [novo1, novo2]
        return []


    # Clipping de poligo Sutherland-Hodgeman
    def __clippingSutherlandHodgeman(self, pontos):
        novosPontos = []
        for i in range(len(pontos)):
            i1 = (i+1)%len(pontos)
            # ambos dentro
            if self.__dentroWindow(pontos[i]) and self.__dentroWindow(pontos[i1]):
                novosPontos.append(pontos[i])
            # primeiro dentro, segundo fora, adiciono o primeiro e mais o da borda
            elif self.__dentroWindow(pontos[i]):
                novos = self.__clippingCohenSutherland(pontos[i], pontos[i1])
                if novos != []:
                    novosPontos.append(pontos[i])
                    novosPontos.append(novos[1])
            # primeiro fora, segundo dentro, adiciono o da borda
            elif self.__dentroWindow(pontos[i1]):
                novos = self.__clippingCohenSutherland(pontos[i], pontos[i1])
                if novos != []:
                    novosPontos.append(novos[0])
            # ambos fora
            else:
                novos = self.__clippingCohenSutherland(pontos[i], pontos[i1])
                if novos != []:
                    novosPontos.append(novos[0])
                    novosPontos.append(novos[1])
                else:
                    # corta a diagonal
                    pos1 = self.__posicao(pontos[i])
                    pos2 = self.__posicao(pontos[i1])
                    if pos1 != pos2:
                        diag = [pos1[i] or pos2[i] for i in range(4)]
                        n = 0
                        if   diag[2] and diag[1]: n = 0 # esq top
                        elif diag[0] and diag[1]: n = 1 # esq top
                        elif diag[0] and diag[3]: n = 3 # dir bot
                        elif diag[2] and diag[3]: n = 2 # dir top
                        novosPontos.append(self.__pontosViewport[n])
        # remove pontos iguais
        novosPontosOtimizados = novosPontos.copy()
        for i in range(len(novosPontos)-1):
            if novosPontos[i].X() == novosPontos[i+1].X() and novosPontos[i].Y() == novosPontos[i+1].Y():
                novosPontosOtimizados.remove(novosPontos[i+1])
        return novosPontosOtimizados

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