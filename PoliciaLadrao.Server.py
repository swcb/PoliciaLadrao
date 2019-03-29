import pygame
import rpyc
import numpy as np
import Objetos


class policiaLadraoServidor(rpyc.Service):

    def __init__(self):
        self.jogadores = []
        self.exposed_Killmoeda = ""
        self.exposed_fim = False
        self.jogador = -1
        self.ladroes = 0
        self.exposed_pos_x = [620/31, (620 / 31) * 29]
        self.exposed_pos_y = [261/13, (261 / 13) * 11]
        self.exposed_x = [1,29]
        self.exposed_y = [1,11]


    def on_connect(self, conn):
        print('   ~Conectado')
        pass

    def on_disconnect(self, conn):
        print('   ~Desconectado')
        pass

    def exposed_getIndole(self):
        print(len(self.jogadores))
        if (len(self.jogadores) % 2 == 1):
            return "policia"
        else:
            self.ladroes += 1
            return "ladrao"

    def exposed_getCredenciais(self, jog, indole):
        self.jogador += 1
        obj = {'posicao': jog, 'indole': indole, 'vivo': True}
        self.jogadores.append(obj)
        print(jog)
        print(self.jogadores)
        return self.jogador

    def exposed_getJogadores(self):
        return self.jogadores

    def exposed_putJogador(self, indice, new):
        try:
            self.jogadores[indice]['posicao'] = new
            return True
        except:
            return False

    def exposed_setKillmoeda(self, moeda):
        self.exposed_Killmoeda = moeda

    def exposed_delJogador(self, indice):
        self.jogadores[indice]['vivo'] = False

'''
    #Verifica se a posição que o jogador
    #deseja ir é permitida
    def verificaMov(self,x,y,z):
        if self.campo[x,y] == 'C':
            if z == 0:
                self.pegaChave(x,y)
            return True
        if self.campo[x,y] == ' ':
            return True
        elif z == 0 and self.campo[x, y] == '/':
            return True
        else:
            return False


    #Verifica se em uma area em formato
    #de cruz ao policial há um ladrao
    #e se o ladrao pegou 5 chaves
    #qualquer um do dois resulta no fim
    def exposed_verificaFim(self):
        if self.jogadorY[1] == self.jogadorY[0] and (self.jogadorX[1]+1 == self.jogadorX[0]   or self.jogadorX[1] - 1 == self.jogadorX[0]):#fixa Y e verifica X -
            return True
        elif  self.jogadorX[1] == self.jogadorX[0] and (self.jogadorY[1] + 1 == self.jogadorY[0] or self.jogadorY[1] - 1 == self.jogadorY[0]):#fixa X e verifica Y !
            return True
        elif self.jogadorX[1] == self.jogadorX[0] and self.jogadorY[1] == self.jogadorY[0]:#Verifica na mesma posicao
            return True
        elif self.qtChaves == 5:
            return True
        return False

    #Aumenta a quantidade de chaves pegas em 1
    #guarda a posição da chave em chavesPegas[]
    def pegaChave(self,x,y):
        self.chavesPega.append(x)
        self.chavesPega.append(y)
        self.qtChaves = self.qtChaves + 1
        self.exposed_carregaCampo()




    #Realiza o movimento para Cima
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movCima(self,z):
        if self.verificaMov(self.jogadorX[z] - 1, self.jogadorY[z], z) == True:
            self.jogadorX[z] = self.jogadorX[z] - 1
            self.exposed_carregaCampo()

    # Realiza o movimento para Baixo
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movBaixo(self, z):
        if self.verificaMov(self.jogadorX[z]+1, self.jogadorY[z], z) == True:
            self.jogadorX[z] = self.jogadorX[z] + 1
            self.exposed_carregaCampo()

    #Realiza o movimento para a Esquerda
    #Chama a função Verifica
    #para a possibilidade do movimento
    def exposed_movEsquerda(self, z):
        if self.verificaMov(self.jogadorX[z], self.jogadorY[z] -1, z) == True:
            self.jogadorY[z] = self.jogadorY[z] - 1
            self.exposed_carregaCampo()

    #Realiza o movimento para a Direita
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movDireita(self, z):
        if self.verificaMov(self.jogadorX[z], self.jogadorY[z] + 1, z) == True:
            self.jogadorY[z] = self.jogadorY[z] + 1
            self.exposed_carregaCampo()
'''


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(policiaLadraoServidor(), port=18861)
    t.start()
