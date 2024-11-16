import pymunk
import pygame

from node_types.physics_shape import PhysicsShape
from scripting.kinematic_body_engine_interactable import KinematicBodyEngineInteractable

# TODO: Move some of this code into its own class class.
class KinematicBody(PhysicsShape):
    def __init__(self):
        PhysicsShape.__init__(self)

        # Set node type
        self.node_type = "KinematicBody"

        self.added_to_simulation = False
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        self.use_move_and_slide = False
        self.use_move_and_collide = False

    def editor_update(self, origin_offset):
        super().editor_update(origin_offset)

    def game_update(self, pymunk_space: pymunk.Space):
        PhysicsShape.game_update(self)

        self.body.velocity = (self.velocity.x, self.velocity.y)

        if not self.added_to_simulation:
            self.body.position = (self.global_position.x, self.global_position.y)
            self.body.angle = self.rotation
            
            self.shape = self.generate_shape()
            pymunk_space.add(self.body, self.shape)

            self.added_to_simulation = True
        
        self.position = pygame.Vector2(self.body.position.x, self.body.position.y) - (pygame.Vector2(0, 0) if self.parent == "Root" else self.parent.get_global_position())
    
    def update_variables_from_interactable(self, engine_interactable: KinematicBodyEngineInteractable):
        super().update_variables_from_interactable(engine_interactable)

        self.velocity = engine_interactable.velocity
        self.use_move_and_collide = engine_interactable.use_move_and_collide
        self.use_move_and_slide = engine_interactable.use_move_and_slide
    
    def generate_engine_interactable(self):
        return KinematicBodyEngineInteractable(
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
            self.velocity,
            self.use_move_and_slide,
            self.use_move_and_collide
        )

    def get_properties_dict(self):
        shape_properties_dict = super().get_properties_dict()
        shape_properties_dict["type"] = "KinematicBody"

        return shape_properties_dict
    
    def load_self(self, node):
        super().load_self(node)
