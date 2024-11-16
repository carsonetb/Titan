from scripting.shape_engine_interactable import ShapeEngineInteractable

class RigidBodyEngineInteractable(ShapeEngineInteractable):
    def __init__(self, children, parent, position, global_position, rotation, scale, shape_index, width, height, radius, points, color, body):
        ShapeEngineInteractable.__init__(self, children, parent, position, global_position, rotation, scale, shape_index, width, height, radius, points, color)

        self.body = body
        
        
        