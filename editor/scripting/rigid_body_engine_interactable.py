from scripting.shape_engine_interactable import ShapeEngineInteractable

class RigidBodyEngineInteractable(ShapeEngineInteractable):
    def __init__(self, children, parent, name, position, global_position, rotation, scale, shape_index, width, height, radius, points, color, velocity, mass, friction, bounciness):
        ShapeEngineInteractable.__init__(self, children, parent, name, position, global_position, rotation, scale, shape_index, width, height, radius, points, color)

        self.velocity = velocity
        self.mass = mass
        self.friction = friction
        self.bounciness = bounciness