import pygame
import pymunk

from resources import global_enumerations
from node_types.shape import Shape

class PhysicsShape(Shape):
    def __init__(self):
        Shape.__init__(self)

        # Set node type
        self.node_type = "PhysicsShape"

        # Set color transparency
        self.color = (self.color[0], self.color[1], self.color[2], 100)

        # Velocity of physics shape, for more advanced physics nodes which
        # inherit the base physics shape.
        # If value of this is not zero, this will be initial velocity.
        self.velocity = pygame.Vector2(0, 0)

    def editor_update(self, origin_offset):
        super().editor_update(origin_offset)
    
    def game_update(self):
        Shape.game_update(self)
    
    def generate_shape(self):
        if self.shape_index == global_enumerations.SHAPE_RECT:
            shape = pymunk.Poly(self.body, [
                (-self.width / 2, self.height / 2),
                (self.width / 2, self.height / 2),
                (-self.width / 2, -self.height / 2),
                (self.width / 2, -self.height / 2)
            ])

        if self.shape_index == global_enumerations.SHAPE_CIRCLE:
            shape = pymunk.Circle(self.body, self.radius)

        if self.shape_index == global_enumerations.SHAPE_POLYGON:
            shape = pymunk.Poly(self.body, self.points)
        
        return shape

    def get_properties_dict(self):
        shape_properties_dict = super().get_properties_dict()
        shape_properties_dict["type"] = "PhysicsShape"
        shape_properties_dict["vel_x"] = self.velocity.x
        shape_properties_dict["vel_y"] = self.velocity.y

        return shape_properties_dict
    
    def load_self(self, node):
        super().load_self(node)

        self.velocity = pygame.Vector2(int(node["vel_x"]), int(node["vel_y"]))
