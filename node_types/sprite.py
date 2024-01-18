import pygame
from node_types.position import Position


class Sprite(Position):
    def __init__(self, sprite_path):
        self.sprite_path = sprite_path
        self.image = pygame.image.load(self.sprite_path).convert_alpha()
        self.node_type = "Sprite"

        Position.__init__(self)

    def editor_update(self, window, origin_offset):
        window.blit(self.image, origin_offset + self.position - pygame.Vector2(self.image.get_width() / 2, self.image.get_height() / 2))

        super().editor_update(window, origin_offset)

    def game_update(self, window):
        window.blit(self.image, self.position - pygame.Vector2(self.image.get_width() / 2, self.image.get_height() / 2))

        super().game_update(window)

    def get_properties_dict(self):
        return {
            "type": "Position", 
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x,
            "position_y": self.position.y, 
            "sprite_path": self.sprite_path
        }