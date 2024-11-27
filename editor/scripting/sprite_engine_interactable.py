from scripting.position_engine_interactable import PositionEngineInteractable
from resources.math.vector2 import Vector2

class SpriteEngineInteractable(PositionEngineInteractable):
    def __init__(self, children, parent, name, position, global_position, rotation, scale, sprite_path, image_width, image_height):
        PositionEngineInteractable.__init__(self, children, parent, name, position, global_position, rotation, scale)

        self.sprite_path = sprite_path
        self.dimensions = Vector2(image_width, image_height)

        