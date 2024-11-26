import raylib
import importlib
import sys
import copy

from resources.math.vector2 import Vector2
import resources.misc
from scripting.position_engine_interactable import PositionEngineInteractable

class Position:
    def __init__(self):
        self.script_path = ""
        self.script = None
        self.node_type = "Position"
        self.position = Vector2(0, 0)
        self.global_position = Vector2(0, 0)
        self.scale = Vector2(1, 1)
        self.previous_scale = Vector2(1, 1)
        self.previous_position = Vector2(0, 0)
        self.previous_rotation = 0
        self.rotation = 0
        self.rotation_degrees = 0
        self.children = []
        self.parent = "Root"
        self.script_has_update = "Untested"
        self.script_has_position = "Untested"
        self.has_script = False
        self.mouse_dragging = False
        self.name = "Unnamed"
        self.first_game_update = True
        self.selected = False
        self.just_moved = False
        self.eligable_for_dragging = False

    def load_script(self, script_path):
        spec = importlib.util.spec_from_file_location("test_script", script_path)
        script = importlib.util.module_from_spec(spec)
        sys.modules["test_script"] = script
        spec.loader.exec_module(script)

        try:
            if script.NODE_TYPE == self.node_type:
                self.script_path = script_path
                self.script = script
                self.has_script = True
                return 
            else:
                print(f"Error Loading Script: NODE_TYPE variable is not the same as '{self.node_type}' type.")
                return
        except:
            print(f"Error Loading Script: NODE_TYPE variable does not exist. It should be '{self.node_type}'")
    
    def editor_update(self, origin_offset=Vector2(0, 0)):
        offset_position = origin_offset + self.global_position
        raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 15, (0, 0, 0, 255))
        
        if self.selected:
            raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 18, (0, 0, 0, 255))

        mouse_pos = raylib.GetMousePosition()
        mouse_pos = Vector2(mouse_pos.x, mouse_pos.y)

        if self.selected and offset_position.distance_to(mouse_pos) < 30:
            raylib.DrawCircle(int(offset_position.x), int(offset_position.y), 15, (0, 0, 0, 255))

            if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                self.eligable_for_dragging = True

            if raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT) and self.eligable_for_dragging:
                self.mouse_dragging = True
            else:
                self.mouse_dragging = False
        else:
            self.eligable_for_dragging = False
        
        if self.mouse_dragging:
            self.position = mouse_pos - origin_offset - (Vector2(0, 0) if self.parent == "Root" else self.parent.get_global_position())

        for child in self.children:
            child.add_scale(self.scale - self.previous_scale)
            child.editor_update(origin_offset)

        if self.position != self.previous_position:
            self.just_moved = True
        else:
            self.just_moved = False

        self.global_position = self.get_global_position()
        self.previous_position = copy.copy(self.position)
        self.previous_scale = copy.copy(self.scale)
    
    def game_update(self):
        self.script_update()

        for child in self.children:
            child.add_scale(self.scale - self.previous_scale)
            child.add_rotation(self.rotation - self.previous_rotation)
            child.game_update()
        
        self.global_position = self.get_global_position()
        self.previous_position = copy.copy(self.position)
        self.previous_scale = self.scale
        self.previous_rotation = self.rotation
    
    def script_update(self):
        engine_interactable = self.generate_engine_interactable()

        if self.has_script:
            if self.script_has_update == "Untested":
                try: 
                    self.script.update(engine_interactable)
                    self.script_has_update = True 
                    try:
                        self.script.ready(engine_interactable)
                    except:
                        pass

                except Exception as e:
                    self.script_has_update = False

            elif self.script_has_update:
                self.script.update(engine_interactable)
            
            self.update_variables_from_interactable(engine_interactable)

    def update_variables_from_interactable(self, engine_interactable):
        self.position = engine_interactable.position
        self.rotation = engine_interactable.rotation
        self.scale = engine_interactable.scale
        
    def generate_engine_interactable(self):
        return PositionEngineInteractable(
            self.children, 
            self.parent, 
            self.position,
            self.global_position, 
            self.rotation, 
            self.scale, 
        )
    
    def add_position(self, added_position):
        self.position += added_position

    def add_scale(self, added_scale: Vector2):
        if added_scale == Vector2(0, 0):
            return

        self.scale += added_scale

        for child in self.children:
            child.add_scale(added_scale)
            child.position += Vector2((child.position - self.position).x * added_scale.x, (child.position - self.position).y * added_scale.y)

    def add_rotation(self, added_rotation: float):
        self.rotation += added_rotation
        self.rotation_degrees = resources.misc.rad_to_deg(self.rotation)

        for child in self.children:
            position_to_rotate = child.position - self.position
            rotated_position = position_to_rotate.rotate_rad(added_rotation)
            child.position = self.position + rotated_position
            child.add_rotation(added_rotation)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_children_recursive(self):
        children = [self]

        for child in self.children:
            children.append(child.get_children_recursive())

        return children

    def get_properties_dict(self):
        return {
            "type": "Position", 
            "name": self.name,
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x, 
            "position_y": self.position.y,
            "rotation": self.rotation,
            "scale_x": self.scale.x,
            "scale_y": self.scale.y,
        }
    
    def get_global_position(self):
        if not self.parent == "Root":
            return self.parent.get_global_position() + self.position
        
        return self.position

    def load_self(self, node):
        self.script_path = node["script_path"]
        self.position = Vector2(node["position_x"], node["position_y"])
        self.scale = Vector2(node["scale_x"], node["scale_y"])
        self.rotation = node["rotation"]
        self.rotation_degrees = resources.misc.misc.rad_to_deg(self.rotation)
        
        self.name = node["name"]
        print(f"INFO: Loaded Position {self.position} name {self.name}")

        if self.script_path:
            self.load_script(self.script_path)

        for child in node["children"]:
            # We have to import these here to avoid circular imports.
            from node_types.sprite import Sprite
            from node_types.shape import Shape
            from node_types.physics_shape import PhysicsShape
            from node_types.rigid_body import RigidBody
            from node_types.static_body import StaticBody

            if child["type"] == "Position":
                node_to_add = Position()
            elif child["type"] == "Sprite":
                node_to_add = Sprite()
            elif child["type"] == "Shape":
                node_to_add = Shape()
            elif child["type"] == "PhysicsShape":
                print("WARNING: Trying to instantiate node of type PhysicsShape. Please don't.")
                node_to_add = PhysicsShape()
            elif child["type"] == "RigidBody":
                node_to_add = RigidBody()
            elif child["type"] == "StaticBody":
                node_to_add = StaticBody()

            node_to_add.load_self(child)
            node_to_add.previous_position = node_to_add.position
            node_to_add.previous_scale = node_to_add.scale
            node_to_add.parent = self
            self.children.append(node_to_add)
