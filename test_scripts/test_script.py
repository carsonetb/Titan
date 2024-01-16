import pygame

NODE_TYPE = "Position"
position = pygame.Vector2(0, 0)


def update():
    global position

    position += pygame.Vector2(1, 1)

def ready():
    position = pygame.Vector2(100, 100)