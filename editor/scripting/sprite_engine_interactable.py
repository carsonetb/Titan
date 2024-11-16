from scripting.position_engine_interactable import PositionEngineInteractable
import pygame

class SpriteEngineInteractable(PositionEngineInteractable):
    def __init__(self, children, parent, position, global_position, rotation, scale, sprite_path, image_width, image_height):
        PositionEngineInteractable.__init__(self, children, parent, position, global_position, rotation, scale)

        self.sprite_path = sprite_path
        self.dimensions = pygame.Vector2(image_width, image_height)

        