import raylib

from resources.math.vector2 import Vector2
from node_types.position import Position
from scripting.sprite_engine_interactable import SpriteEngineInteractable

class Sprite(Position):
    def __init__(self):
        Position.__init__(self)

        self.sprite_path = None
        self.image = None
        self.node_type = "Sprite"
        self.image_width = None
        self.image_height = None

    def editor_update(self, origin_offset):
        super().editor_update(origin_offset)

        offset_position = self.global_position + origin_offset

        if self.sprite_path:
            raylib.DrawTexturePro(self.image, [0.0, 0.0, self.image_width, self.image_height], [int(offset_position.x), int(offset_position.y), self.image_width * self.scale.x, self.image_height * self.scale.y], [self.image_width / 2 * self.scale.x, self.image_height / 2 * self.scale.y], self.rotation_degrees, raylib.WHITE)

    def game_update(self):
        super().game_update()

        # Draw sprite to screen.
        if self.sprite_path:
            dimensions = [0.0, 0.0, self.image_width, self.image_height]
            scaled_position = Vector2(int(self.global_position.x - (self.image_width * self.scale.x) / 2), int(self.global_position.y - (self.image_height * self.scale.y) / 2))
            scaled_dimensions = Vector2(self.image_width * self.scale.x, self.image_height * self.scale.y)
            raylib.DrawTexturePro(self.image, dimensions, [scaled_position.x, scaled_position.y, scaled_dimensions.x, scaled_dimensions.y], [0, 0], self.rotation_degrees, raylib.WHITE)

    def generate_engine_interactable(self):
        return SpriteEngineInteractable(
            self.children, 
            self.parent, 
            self.position,
            self.global_position, 
            self.rotation, 
            self.scale, 
            self.sprite_path,
            self.image_width,
            self.image_height,
        )

    def set_texture(self, path):
        self.sprite_path = path
        image = raylib.LoadImage(bytes(self.sprite_path, "utf-8"))
        self.image = raylib.LoadTextureFromImage(image)
        self.image_width = image.width
        self.image_height = image.height
        raylib.UnloadImage(image)

    def get_properties_dict(self):
        return {
            "type": "Sprite", 
            "name": self.name,
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x,
            "position_y": self.position.y, 
            "scale_x": self.scale.x,
            "scale_y": self.scale.y,
            "rotation": self.rotation,
            "sprite_path": self.sprite_path if self.sprite_path else "None"
        }
    
    def load_self(self, node):
        super().load_self(node)
    
        self.sprite_path = node["sprite_path"] if node["sprite_path"] != "None" else None
        if self.sprite_path:
            self.set_texture(self.sprite_path)
