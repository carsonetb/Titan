from scripting.shape_engine_interactable import ShapeEngineInteractable

class KinematicBodyEngineInteractable(ShapeEngineInteractable):
    def __init__(self, children, parent, name, position, global_position, rotation, scale, shape_index, width, height, radius, points, color, velocity, use_move_and_slide, use_move_and_collide):
        ShapeEngineInteractable.__init__(self, children, parent, name, position, global_position, rotation, scale, shape_index, width, height, radius, points, color)

        self.velocity = velocity
        self.use_move_and_slide = use_move_and_slide
        self.use_move_and_collide = use_move_and_collide
        
