import pygame
import raylib

NODE_TYPE = "Position"
position = pygame.Vector2(100, 0)


def update(delta, engine_interactable):
    global position

    if engine_interactable.is_key_pressed(engine_interactable.KEY_A):
        position.x -= 1 * delta * 60
    if engine_interactable.is_key_pressed(engine_interactable.KEY_D):
        position.x += 1 * delta * 60
    if engine_interactable.is_key_pressed(engine_interactable.KEY_W):
        position.y -= 1 * delta * 60
    if engine_interactable.is_key_pressed(engine_interactable.KEY_S):
        position.y += 1 * delta * 60

def ready():
    global position

    position = pygame.Vector2(100, 100)