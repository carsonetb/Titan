import pymunk

import resources.global_enumerations as global_enumerations
from node_types.physics_shape import PhysicsShape

# TODO: Move some of this code into its own class class.
class StaticBody(PhysicsShape):
    def __init__(self):
        PhysicsShape.__init__(self)

        # Set node type
        self.node_type = "StaticBody"

        self.added_to_simulation = False
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

    def editor_update(self, origin_offset):
        super().editor_update(origin_offset)

    def game_update(self, pymunk_space: pymunk.Space):
        PhysicsShape.game_update(self)

        self.body.position = (self.global_position.x, self.global_position.y)
        self.body.angle = self.rotation

        if not self.added_to_simulation:
            self.shape = self.generate_shape()
            
            self.shape.friction = 0.9
            self.shape.elasticity = 0.1
            pymunk_space.add(self.body, self.shape)

            self.added_to_simulation = True

    def get_properties_dict(self):
        shape_properties_dict = super().get_properties_dict()
        shape_properties_dict["type"] = "StaticBody"

        return shape_properties_dict
    
    def load_self(self, node):
        super().load_self(node)
