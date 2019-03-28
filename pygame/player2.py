import pygame, rpyc, time, sys

def main():
    c = rpyc.connect("localhost", 18861)
    pygame.init()
    jogador = 2
    size = width, height = 820,600
    screen = pygame.display.set_mode(size)
    black = 255, 255, 255
    finish = pygame.image.load("images\\finish.png")
    finishrect = finish.get_rect().move([160,0])
    car1 = pygame.image.load("cars\\p1.png")
    car1rect = car1.get_rect()
    car2 = pygame.image.load("cars\\p2.png")
    car2rect = car2.get_rect()
    road = pygame.image.load("images\\road.jpg")
    roadrect = road.get_rect().move([160,-5])
    grass = pygame.image.load("images\\grass.png")
    grassrect = grass.get_rect().move([0,0])
    car1rect = car1rect.move([450,500])
    car2rect = car2rect.move([250,500])
    speed = [0,-500/15]
    error_sound = pygame.mixer.Sound("sounds\error.wav")
    cont = 0
    pos1 = 0
    load = 0
    acertou = 0
    errou = 0
    n1 = pygame.image.load("icos\\number-1.png")
    n2 = pygame.image.load("icos\\number-1.png")
    n3 = pygame.image.load("icos\\number-1.png")
    n4 = pygame.image.load("icos\\number-1.png")
    n5 = pygame.image.load("icos\\number-1.png")
    n1rect = n1.get_rect().move([3,10])
    n2rect = n2.get_rect().move([35,10])
    n3rect = n3.get_rect().move([67,10])
    n4rect = n4.get_rect().move([99,10])
    n5rect = n5.get_rect().move([131,10])
    c.root.comeca()
    while c.root.get_winner() == 0:
        #n1 = pygame.image.load("C:\Mikael\PPC\pygame\\number-"+str(seq[0])+".png")
        if(load == 0):
            seq = c.root.get_seq(jogador)
            if(acertou):
                time.sleep(0.5)
                acertou = 0
            if(errou):
                time.sleep(1.5)
                errou = 0
            n1 = pygame.image.load("icos\\number-"+str(seq[0])+".png")
            n2 = pygame.image.load("icos\\number-"+str(seq[1])+".png")
            n3 = pygame.image.load("icos\\number-"+str(seq[2])+".png")
            if(c.root.get_cont(jogador) > c.root.get_end()/2):
                n4 = pygame.image.load("icos\\number-"+str(seq[3])+".png")
                n5 = pygame.image.load("icos\\number-"+str(seq[4])+".png")
            load = 1
        
        n1rect = n1.get_rect().move([3,10])
        n2rect = n2.get_rect().move([35,10])
        n3rect = n3.get_rect().move([67,10])
        if(c.root.get_cont(jogador) > c.root.get_end()/2):
            n4rect = n4.get_rect().move([99,10])
            n5rect = n5.get_rect().move([131,10])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                _ = pygame.key.name(event.key)
                try:
                    if(int(_[1]) == seq[cont]):
                        cont = cont + 1
                        if(cont == 1):
                            n1 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n1rect = n1.get_rect().move([3,10])
                        if(cont == 2):
                            n2 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n2rect = n2.get_rect().move([35,10])
                        if(cont == 3):
                            n3 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n3rect = n3.get_rect().move([67,10])
                        if(c.root.get_cont(jogador) > c.root.get_end()/2):
                            if(cont == 4):
                                n4 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                                n4rect = n4.get_rect().move([99,10])
                            if(cont == 5):
                                n5 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                                n5rect = n5.get_rect().move([131,10])
                    else:
                        if pygame.mixer and pygame.mixer.get_init():
                            error_sound.play()
                        if(cont == 0):
                            n1 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n1rect = n1.get_rect().move([3,10])
                        if(cont == 1):
                            n2 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n2rect = n2.get_rect().move([35,10])
                        if(cont == 2):
                            n3 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n3rect = n3.get_rect().move([67,10])
                        if(c.root.get_cont(jogador) > c.root.get_end()/2):
                            if(cont == 3):
                                n4 = pygame.image.load("icos\\denied-"+str(seq[cont-1])+".png")
                                n4rect = n4.get_rect().move([99,10])
                            if(cont == 4):
                                n5 = pygame.image.load("icos\\denied-"+str(seq[cont-1])+".png")
                                n5rect = n5.get_rect().move([131,10])

                        c.root.gera_seq(jogador)
                        errou = 1
                        cont = 0
                        load = 0
                    
                    if(c.root.get_cont(jogador) <= c.root.get_end()/2):
                        if(cont == 3):
                            c.root.anda(jogador)
                            car2rect = car2rect.move(speed)
                            cont = 0
                            load = 0
                            acertou = 1
                    else:
                        if(cont == 5):
                            c.root.anda(jogador)
                            car2rect = car2rect.move(speed)
                            cont = 0
                            load = 0
                            acertou = 1
                except:
                    pass
        cont1 = c.root.get_cont(1)
        if(cont1 != pos1):
            aux = 500 + cont1*speed[1]
            car1rect = car1.get_rect().move([450, aux])
            pos1 = cont1
        
        screen.fill(black)
        screen.blit(grass, grassrect)
        screen.blit(road, roadrect)
        screen.blit(finish, finishrect)
        screen.blit(car1, car1rect)
        screen.blit(car2, car2rect)
        screen.blit(n1, n1rect)
        screen.blit(n2, n2rect)
        screen.blit(n3, n3rect)
        if(c.root.get_cont(jogador) > c.root.get_end()/2):
            screen.blit(n4, n4rect)
            screen.blit(n5, n5rect)
        pygame.display.flip()
    
    confirm = 0
    while(not confirm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                confirm = 1
        
        screen.fill(black)
        screen.blit(grass, grassrect)
        screen.blit(road, roadrect)
        screen.blit(finish, finishrect)
        screen.blit(car1, car1rect)
        screen.blit(car2, car2rect)
        screen.blit(n1, n1rect)
        screen.blit(n2, n2rect)
        screen.blit(n3, n3rect)
        screen.blit(n4, n4rect)
        screen.blit(n5, n5rect)

        vic = pygame.image.load("images\win.png")
        if(c.root.get_winner() != jogador):
            vic = pygame.image.load("images\lose.png")
        
        vicrect = vic.get_rect().move([200,200])
        screen.blit(vic, vicrect)
        pygame.display.flip()

main()
