import pygame

class ladrao(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.image = pygame.image.load("images\\ladrao.png")


class moeda(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.image = pygame.image.load("images\\moeda.png")

class policia(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.image = pygame.image.load("images\\pol.png")

class lose(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.image = pygame.image.load("images\\derrota.png")

class win(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.image = pygame.image.load("images\\vic.png")

class win2(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.image = pygame.image.load("images\\vic2.png")

class wall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.image = pygame.image.load("images\\bloco3.png")