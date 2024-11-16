import pygame
import pymunk
import math

import resources.global_enumerations as global_enumerations
from node_types.physics_shape import PhysicsShape
from scripting.rigid_body_engine_interactable import RigidBodyEngineInteractable

class RigidBody(PhysicsShape):
    def __init__(self):
        PhysicsShape.__init__(self)

        # Set node type
        self.node_type = "RigidBody"

        self.mass = 10
        self.body = pymunk.Body()
        self.added_to_simulation = False

    # Not sure we need to update the shape and stuff in here ...
    def editor_update(self, origin_offset):
        super().editor_update(origin_offset)

        if self.shape_index == global_enumerations.SHAPE_RECT:
            self.shape = pymunk.Poly(self.body, [
                (self.global_position.x - self.width / 2, -self.global_position.y + self.height / 2),
                (self.global_position.x + self.width / 2, -self.global_position.y + self.height / 2),
                (self.global_position.x - self.width / 2, -self.global_position.y - self.height / 2),
                (self.global_position.x + self.width / 2, -self.global_position.y - self.height / 2)
            ])
            self.shape.mass = self.mass

        if self.shape_index == global_enumerations.SHAPE_CIRCLE:
            self.shape = pymunk.Circle(self.body, self.radius)
            self.shape.mass = self.mass

        if self.shape_index == global_enumerations.SHAPE_POLYGON:
            self.shape = pymunk.Poly(self.body, self.points)
            self.shape.mass = self.mass

        self.body.position = (self.global_position.x, -self.global_position.y)
        self.body.angle = self.rotation

    def game_update(self, pymunk_space: pymunk.Space):
        PhysicsShape.game_update(self)

        self.body.mass = self.mass

        if not self.added_to_simulation:
            self.body.position = (self.global_position.x, self.global_position.y)

            self.shape = pymunk.Poly(self.body, [
                (-self.width / 2, self.height / 2),
                (self.width / 2, self.height / 2),
                (-self.width / 2, -self.height / 2),
                (self.width / 2, -self.height / 2)
            ])
            self.shape.mass = self.mass
            self.shape.elasticity = 0
            self.shape.friction = 1

            self.shape.friction = 0.9
            self.shape.elasticity = 0.1
            pymunk_space.add(self.body, self.shape)
            
            self.added_to_simulation = True

        self.position = pygame.Vector2(self.body.position.x, self.body.position.y) - (pygame.Vector2(0, 0) if self.parent == "Root" else self.parent.get_global_position())
        self.rotation = math.atan2(self.body.rotation_vector.y, self.body.rotation_vector.x)
    
    def generate_engine_interactable(self):
        return RigidBodyEngineInteractable(
            self.children, 
            self.parent, 
            self.position,
            self.global_position, 
            self.rotation, 
            self.scale,
            self.shape_index,
            self.width,
            self.height,
            self.radius,
            self.points,
            self.color,
            self.body,
        )

    def get_properties_dict(self):
        shape_properties_dict = super().get_properties_dict()
        shape_properties_dict["type"] = "RigidBody"
        shape_properties_dict["mass"] = self.mass

        return shape_properties_dict
    
    def load_self(self, node):
        super().load_self(node)

        self.mass = int(node["mass"])
