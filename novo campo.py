import pygame
import rpyc
import Objetos


#(40,30)
#800/40  600/30


pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.__PYGAMEinit__
pygame.init()
relogio = pygame.time.Clock()
campo2 = 800, 600

x1 = 800/40
y1 = 600/30

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
for i in range (0,30):
    parede = Objetos.wall(0, y1*i)
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
