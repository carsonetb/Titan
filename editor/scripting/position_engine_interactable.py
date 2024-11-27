from scripting.base_engine_interactable import EngineInteractable
import resources.misc

class PositionEngineInteractable(EngineInteractable):
    def __init__(self, children, parent, name, position, global_position, rotation, scale):
        EngineInteractable.__init__(self, children, parent)

        self.name = name
        self.position = position
        self.global_position = global_position
        self.rotation = rotation
        self.rotation_degrees = resources.misc.misc.rad_to_deg(rotation)
        self.scale = scale

        self._children_dict = {}
        for child in self.children:
            self._children_dict[child.name] = child
    
    def add_child(self, child):
        super().add_child(child)
        self._children_dict[child.name] = child
    
    def remove_child(self, child):
        super().remove_child(child)
        self._children_dict.pop(child.name)
    
    # All this work just so that we can lookup the name
    # from an ultra-efficient hashmap. Nice.
    def get_child(self, name):
        return self._children_dict[name]
        