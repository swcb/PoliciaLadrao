import pygame
import rpyc
import numpy as np
import Objetos

campo_x = 620/31
campo_y = 261/13

class policiaLadraoServidor(rpyc.Service):

    def __init__(self):
        self.jogadores = []
        self.exposed_Killmoeda = ""
        self.exposed_fim = False
        self.exposed_win = 3
        self.jogador = -1
        self.ladroes = 0
        self.cont = 0
        self.exposed_pos_x = [campo_x, campo_x * 29]
        self.exposed_pos_y = [campo_y, campo_y * 11]
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

    def exposed_getIndice(self):
        print(self.exposed_pos_x)
        self.jogador += 1
        return self.jogador

    def exposed_getCredenciais(self, jog, indole):
        obj = {'posicao': jog, 'indole': indole, 'vivo': True}
        self.jogadores.append(obj)
        print(jog)
        print(self.jogadores)
        return 0

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

    def exposed_cont(self):
        self.cont +=1
        print(self.cont)

    def exposed_delJogador(self, indice):
        self.jogadores[indice]['vivo'] = False
        self.ladroes -= 1

    def exposed_getFim(self):
        if self.ladroes == 0:
            self.exposed_win = 0
            return True
        elif self.cont == 5:
            self.exposed_win = 1
            return True
        else:
            return False



if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(policiaLadraoServidor(), port=18861)
    t.start()
