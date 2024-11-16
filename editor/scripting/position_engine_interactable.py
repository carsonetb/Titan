from scripting.base_engine_interactable import EngineInteractable
import resources.misc

class PositionEngineInteractable(EngineInteractable):
    def __init__(self, children, parent, position, global_position, rotation, scale):
        EngineInteractable.__init__(self, children, parent)

        self.position = position
        self.global_position = global_position
        self.rotation = rotation
        self.rotation_degrees = resources.misc.rad_to_deg(rotation)
        self.scale = scale