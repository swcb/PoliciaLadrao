import pygame
import rpyc
import numpy as np
import Objetos
import random
from threading import *

campo_x = 620/31
campo_y = 261/13


def setMoedas( campo):
    for i in range(0, 15):
        condicao = True
        while condicao:
            i = random.randint(0, 40)
            j = random.randint(0, 30)
            if not (campo[j, i] == 1) and not (campo[j, i] == 2) and not (
                    campo[j, i] == 3 and not campo[j, i] == 4):
                campo[j, i] = 4
                condicao = False
        return campo

class policiaLadraoServidor(rpyc.Service):

    def __init__(self):
        self.jogadores = []
        self.exposed_Killmoeda = ""
        self.exposed_fim = False
        self.exposed_win = 3
        self.jogador = -1
        self.ladroes = 0
        self.cont = 0
        self.exposed_campo = self.setCampo()
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

    def setCampo(self):
        campo = np.zeros((31, 41))
        campo[2::2, 2::2] = campo[3::3, 2::6] = 1
        campo[:, 0] = campo[:, 40] = campo[0, :] = campo[30, :] = 1
        campo[29, 16] = campo[29, 24] = campo[1, 16] = campo[1, 24] = 1
        campo[28, 39] = campo[2, 37] = campo[2, 35] = campo[28, 37] = 1
        campo[2::4, 3::7] = campo[4::12, 9] = campo[4::4, 5] = 1
        campo[19, 12] = campo[20, 11] = campo[21, 12] = campo[20, 13] = 1
        campo[23, 22] = campo[20, 21] = campo[19, 24] = campo[22, 25] = 1
        campo[9, 23] = campo[6::4, 37] = campo[8::4, 35] = campo[25, 12] = 1
        campo[7::8, 28] = campo[14, 25] = campo[13, 30] = campo[11, 28] = 1
        campo[24, 7] = campo[22, 9] = campo[5, 6] = campo[8, 9] = campo[11, 12] = 1
        campo[12, 11] = campo[16, 13] = campo[13, 16] = campo[13, 18] = campo[12, 15] = 1
        campo[27, 34] = campo[8::12, 39] = campo[24, 1::38] = campo[25, 4::32] = 1
        campo[25, 16] = campo[23, 18] = 1
        campo[8::12, 1] = campo[6, 13] = campo[7, 18] = campo[6::6, 23] = campo[2, 23] = 1
        campo[28, 3] = campo[6::20, 15] = campo[14, 19] = campo[17, 14] = 2
        campo[21, 23] = campo[7, 22] = campo[23, 6] = campo[16, 27] = 2
        campo[2, 19] = campo[2, 39] = campo[28, 35] = campo[2::16, 5] = 2
        campo[7, 2::32] = campo[16, 39] = 2
        campo[10, 13] = campo[26, 9] = campo[10, 27] = campo[26, 33] = campo[22, 15] = 2

        for i in range(0, 1000):
            condicao = True
            while condicao:
                i = random.randint(0, 40)
                j = random.randint(0, 30)
                print(j, i)
                if campo[j, i] == 0:
                    campo[j, i] = 4
                    condicao = False

        return campo

    def exposed_posicaoInicial(self):
        condicao = True
        while condicao:
            i = random.randint(0, 40)
            j = random.randint(0, 30)
            pos = []
            if not (self.exposed_campo[j, i] == 1) and not (self.exposed_campo[j, i] == 2) and not (self.exposed_campo[j, i] == 3):
                pos.append(i)
                pos.append(j)
                return pos

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
