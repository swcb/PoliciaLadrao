import pygame
import rpyc
import Objetos
import numpy as np


#(40,30)
#800/40  600/30


pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.__PYGAMEinit__
pygame.init()
relogio = pygame.time.Clock()
campo2 = 820, 620

x1 = 820/41
y1 = 620/31


campo = np.zeros((31,41))
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


#Movimentação
dir = [620 / 31, 0]
esq = [-620 / 31, 0]
up = [0, -261 / 13]
down = [0, 261 / 13]

#Tela e Campo
screen = pygame.display.set_mode(campo2)
pygame.display.set_caption("PoliciaLadrao")
black = 0, 0, 0
campo3 = pygame.image.load("images\\campo3.png")
camporect = campo3.get_rect().move([0, 0])

paredes = pygame.sprite.Group()

for i in range(0,31):
    for j in range (0,41):
        if campo [i,j] == 1:
            parede = Objetos.wall(x1 * j, y1 * i)
            paredes.add(parede)
        if campo[i,j] == 2:
            parede = Objetos.wallt(x1 * j, y1 * i)
            paredes.add(parede)

fim = False
while not fim:

    for event in pygame.event.get():
        pygame.key.get_repeat()
        if event.type == pygame.QUIT:
            fim = True

    screen.fill(black)
    screen.blit(campo3, camporect)
    for parede in paredes:
        screen.blit(parede.image, parede.rect)
    pygame.display.flip()
