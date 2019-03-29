from pycuda import driver, compiler, tools

import pygame
import rpyc
import Objetos
import numpy as np
import time
from threading import *


"""
pos_x = 620/31*29
    pos_y = 261/13*11
    px = 29
    py = 11

K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
K_w           w       w
K_a           a       a
K_s           s       s
K_d           d       d
car1rect = car1rect.move(speed)
campo2 = 13 x 31.
"""

fim = False

#Verificacao da movimentacao do policial
def block(px, py, campo):
    if campo[py,px] == 1 or campo[py,px] == 2:
        return True
    else:
        return False


#Verificacao da movimentacao do ladrao
def blockl(px, py, campo):
    if campo[py, px] == 1:
        return True
    else:
        return False


def verificaMoedas(moedas, conn):
        aux = conn.root.Killmoeda
        for moeda in moedas:
            if (moeda.rect == aux):
                moeda.kill()
                cont = cont + 1

#def

#Verifica se algum larao colidiu com
#algum policial
def verificaKillLadrao(conn, indice, indole, derrota):
    joga = conn.root.getJogadores()
    minha = joga[indice]
    if (indole == 'ladrao'):
        for jog in joga:
            if jog['posicao'] == minha['posicao'] and jog['indole'] == 'policia':
                conn.root.delJogador(indice)
                derrota = True
                global fim
                fim = True


def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.__PYGAMEinit__
    pygame.init()
    relogio = pygame.time.Clock()
    campo2 = 620, 261


    #Movimentação
    dir = [620 / 31, 0]
    esq = [-620 / 31, 0]
    up = [0, -261 / 13]
    down = [0, 261 / 13]

    #Tela e Campo
    screen = pygame.display.set_mode(campo2)
    pygame.display.set_caption("PoliciaLadrao")
    black = 0, 0, 0
    campo2 = pygame.image.load("images\\campo2.png")
    camporect = campo2.get_rect().move([0, 0])


    #Posição inicial do jogador
    #trocar para a chamada ao servidor que irá fornecer
    #pos = a posicao usada para desenhar na tela
    #p = posicao na matrix do campo para verificacao da movimentacao
    pos_x = 620/31
    pos_y = 261/13
    px = 1
    py = 1


    #Campo em matriz para criar as paredes internas.
    campo = np.zeros((13,31))
    campo[2::2,2::2] = 1
    campo[2, 3] = campo[2, 19] = campo[2, 27] = 1
    campo[1, 8] = campo[3, 22] = campo[5, 14] = campo[5, 20] = campo[11, 12] = 1
    campo[4, 3] = campo[4, 13] = campo[4, 27] = 1
    campo[6, 1] = campo[6, 7] = campo[6, 23] = campo[6, 29] = 1
    campo[10, 1] = campo[10, 9] = campo[10, 13] = campo[10, 25] = campo[10, 29] = 1
    campo[2, 1] = campo[2, 9] = campo[4, 23] = campo[4, 29] = campo[5, 16] = campo[6, 11] = 2
    campo[7, 4] = campo[9, 18] = campo[10, 3] = campo[10, 11] = campo[10, 27] = 2

    #Criacao do jogador e dos grupos
    #deverá ser feita no servidor
    #e o jogador recebera o seu sprite
    #e todos os grupos
    ladrao = pygame.image.load("images\\ladrao.png")
    policia = pygame.image.load("images\\pol.png")
    moedas = pygame.sprite.Group()
    pos_xMoeda = [pos_x, pos_x*29, pos_x*18, pos_x*13, pos_x*10, pos_x*24, pos_x, pos_x*10]
    pos_yMoeda = [pos_y*11, pos_y, pos_y*7, pos_y*11, pos_y*3, pos_y*5, pos_y*7, pos_y*9]
    for i in range(0,7):
        moeda = Objetos.moeda(pos_xMoeda[i],pos_yMoeda[i])
        moedas.add(moeda)

    #Contador de moedas e condicao para fim
    #o contador sera guardado no servidor
    cont = 0

    #repeticao das teclas
    #em mls (pelo menos o segundo)


    conn = rpyc.connect("localhost", 18861)
    indole = conn.root.getIndole()
    if indole == 'ladrao':
        jog1 = Objetos.ladrao(pos_x,pos_y)
        pygame.key.set_repeat(1, 150)
    else:
        jog1 = Objetos.policia(pos_x,pos_y)
        pygame.key.set_repeat(1, 50)
    print(indole)
    indice = conn.root.getCredenciais(jog1.rect, indole)
    print(indice)
    derrota = False

    kernel_code = """
    __global__ void verificaKillMoeda(moedas, conn, jog1, indole, cont):
    {
    for moeda in moedas:
        if pygame.sprite.collide_rect(jog1, moeda) and indole == 'ladrao':
            moeda.kill()
            cont = cont + 1
            conn.root.setKillmoeda(moeda.rect)
    }
    """
    mod = compiler.SourceModule(kernel_code)
    verificaKillMoeda = mod.get_function("verificakillmoeda")








    global fim

    while not fim:

        inicio = time.time()
        for event in pygame.event.get():
            pygame.key.get_repeat()
            if event.type == pygame.QUIT:
                fim = True
            if event.type == pygame.KEYDOWN:
                if(indole == 'ladrao'):
                    if event.key == pygame.K_UP and not (pos_y - 261/13) <= 0 and not blockl(px,py-1,campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not(pos_y + 261/13 > 261 - (2*261/13)) and not blockl(px,py+1,campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not(pos_x  >= 620 - (2*620/31)) and not blockl(px+1,py,campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + 620/31
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - 620/31 <  620/31) and not blockl(px-1,py,campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - 620/31
                        conn.root.putJogador(indice, jog1.rect)
                else:
                    if event.key == pygame.K_UP and not (pos_y - 261/13) <= 0 and not block(px,py-1,campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not(pos_y + 261/13 > 261 - (2*261/13)) and not block(px,py+1,campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not(pos_x  >= 620 - (2*620/31)) and not block(px+1,py,campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + 620/31
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - 620/31 <  620/31) and not block(px-1,py,campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - 620/31
                        conn.root.putJogador(indice, jog1.rect)
        #Verifica se o jogador passou por uma moeda
        #O servidor tem q fazer isso verificando
        #se algum ladrao passou por moeda

        verificaKillMoeda(moedas, conn, jog1, indole, cont)

        b = Thread(target=verificaKillMoeda(moedas, conn, jog1, indole, cont))
        b.start()

        c = Thread(target=verificaKillLadrao(conn, indice, indole, derrota))
        c.start()

        #Desenho da tela
        screen.fill(black)
        screen.blit(campo2, camporect)
        for moeda in moedas:
            screen.blit(moeda.image,moeda.rect)
        screen.blit(jog1.image, jog1.rect)
        jogadores = conn.root.getJogadores()
        for jogador in jogadores:
            if(jogador['vivo']):
                if(jogador['indole'] == 'ladrao'):
                    screen.blit(ladrao, jogador['posicao'])
                else:
                    screen.blit(policia, jogador['posicao'])
            else:
                print("errou")
        pygame.display.flip()
        relogio.tick(10)
        fim1 = time.time()
        print( (fim1 - inicio)*1000)


    de = pygame.image.load("images\derrota.png")


    confirm = False

    while (not confirm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm = True
            if event.type == pygame.KEYDOWN:
                confirm = 1

        derect = de.get_rect().move([0, 0])

        screen.fill(black)
        screen.blit(campo2, camporect)
        for jogador in jogadores:
            if (jogador['vivo']):
                if (jogador['indole'] == 'ladrao'):
                    screen.blit(jog1.image, jogador['posicao'])
                else:
                    screen.blit(policia, jogador['posicao'])
            else:
                print("errou")
        screen.blit(de, derect)
        pygame.display.flip()



    #pygame.quit()
    print(cont)
main()