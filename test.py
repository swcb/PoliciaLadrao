import pygame
import rpyc
import Objetos
from threading import *
import numpy as np
import random


def criaMoedas(moedas, conn, campo):
    x1 = 820 / 41
    y1 = 620 / 31
    for i in range(0, 15):

        condicao = True
        while condicao:
            i = random.randint(0, 40)
            j = random.randint(0, 30)
            if not (campo[j, i] == 1) and not (campo[j, i] == 2) and not (
                    campo[j, i] == 3 and not campo[j, i] == 4):
                moeda = Objetos.moeda(x1 * i, y1 * j)
                moedas.add(moeda)
                condicao = False



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

def main():
    # Movimentação
    dir = [620 / 31, 0]
    esq = [-620 / 31, 0]
    up = [0, -261 / 13]
    down = [0, 261 / 13]

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.__PYGAMEinit__
    pygame.init()
    relogio = pygame.time.Clock()
    tamanhoCampo = 820, 620

    x1 = 820/41
    y1 = 620/31

    conn = rpyc.connect("localhost", 18861)
    indole = conn.root.getIndole()
    indice = conn.root.getIndice()
    campo = conn.root.campo
    pos = conn.root.posicaoInicial()
    px = pos[0]
    py = pos[1]
    pos_x = pos[0] * x1
    pos_y = pos[1] * y1
    if indole == 'ladrao':
        jog1 = Objetos.ladrao(pos[0] * x1, pos[1] * y1)
        pygame.key.set_repeat(250)
    else:
        jog1 = Objetos.policia(pos[0], pos[1])
        pygame.key.set_repeat(150)
    conn.root.getCredenciais(jog1.rect, indole)
    screen = pygame.display.set_mode(tamanhoCampo)
    pygame.display.set_caption("PoliciaLadrao")
    black = 0, 0, 0
    campo3 = pygame.image.load("images\\campo3.png")
    camporect = campo3.get_rect().move([0, 0])

    paredes = pygame.sprite.Group()
    moedas = pygame.sprite.Group()

    #a = Thread(target=criaMoedas(moedas, campo))
    #a.start()


    for i in range(0, 31):
        for j in range (0, 41):
            if campo[i, j] == 1:
                parede = Objetos.wall(x1 * j, y1 * i)
                paredes.add(parede)
            if campo[i, j] == 2:
                parede = Objetos.wallt(x1 * j, y1 * i)
                paredes.add(parede)
            if campo[i, j] == 4:
                moeda = Objetos.moeda(x1 * i, y1 * j)
                moedas.add(moeda)

    fim = False
    while not fim:
        for event in pygame.event.get():
            pygame.key.get_repeat()
            if event.type == pygame.QUIT:
                fim = True
            if event.type == pygame.KEYDOWN:
                if (indole == 'ladrao'):
                    if event.key == pygame.K_UP and not (pos_y - y1) <= 0 and not blockl(px, py - 1, campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - y1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not (pos_y + y1 > 620 - (2 * y1)) and not blockl(px, py + 1, campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + y1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not (pos_x >= 820 - (2 * x1)) and not blockl(px + 1, py, campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + x1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - x1 < x1) and not blockl(px - 1, py, campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - x1
                        conn.root.putJogador(indice, jog1.rect)
                else:
                    if event.key == pygame.K_UP and not (pos_y - y1) <= 0 and not block(px, py - 1, campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - y1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not (pos_y + y1 > 620 - (2 * y1)) and not block(px, py + 1, campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + y1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not (pos_x >= 820 - (2 * x1)) and not block(px + 1, py, campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + x1
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - x1 < x1) and not block(px - 1, py, campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - x1
                        conn.root.putJogador(indice, jog1.rect)


        screen.fill(black)
        screen.blit(campo3, camporect)
        for parede in paredes:
            screen.blit(parede.image, parede.rect)
        for moeda in moedas:
            screen.blit(moeda.image, moeda.rect)
        screen.blit(jog1.image, jog1.rect)
        pygame.display.flip()
        relogio.tick(30)

main()