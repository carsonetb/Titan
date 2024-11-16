from scripting.position_engine_interactable import PositionEngineInteractable
import pygame

class ShapeEngineInteractable(PositionEngineInteractable):
    def __init__(self, children, parent, position, global_position, rotation, scale, shape_index, width, height, radius, points, color):
        PositionEngineInteractable.__init__(self, children, parent, position, global_position, rotation, scale)
        
        self.shape_type = shape_index
        self.rect_dimensions = pygame.Vector2(width, height)
        self.circle_radius = radius
        self.points = points
        self.color = color
        