from scripting.position_engine_interactable import PositionEngineInteractable

class ShapeEngineInteractable(PositionEngineInteractable):
    def __init__(self, children, parent, position, global_position, rotation, scale, shape_index, width, height, radius, points, color):
        PositionEngineInteractable.__init__(self, children, parent, position, global_position, rotation, scale)
        
        self.shape_type = shape_index
        self.rect_width = width
        self.rect_width = height
        self.circle_radius = radius
        self.points = points
        self.color = color
        