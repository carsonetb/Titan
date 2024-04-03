import pygame
import raylib
import importlib
import sys
from pygame import gfxdraw
import random

class Position:
    def __init__(self):
        self.script_path = ""
        self.script = None
        self.node_type = "Position"
        self.position = pygame.Vector2(0, 0)
        self.previous_position = pygame.Vector2(0, 0)
        self.scale = pygame.Vector2(1, 1)
        self.previous_scale = pygame.Vector2(1, 1)
        self.children = []
        self.parent = "Root"
        self.script_has_update = "Untested"
        self.script_has_position = "Untested"
        self.has_script = False
        self.mouse_dragging = False
        self.name = "Unnamed"
        self.first_game_update = True
        self.selected = False

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
    
    def editor_update(self, origin_offset):
        offset_position = origin_offset + self.position
        raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 15, (0, 0, 0, 255))
        
        if self.selected:
            raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 18, (0, 0, 0, 255))

        mouse_pos = raylib.GetMousePosition()
        mouse_pos = pygame.Vector2(mouse_pos.x, mouse_pos.y)

        if self.selected and offset_position.distance_to(mouse_pos) < 30:
            raylib.DrawCircle(int(offset_position.x), int(offset_position.y), 15, (0, 0, 0, 255))

            if raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT):
                self.mouse_dragging = True
            else:
                self.mouse_dragging = False
        
        if self.mouse_dragging:
            self.position = mouse_pos - origin_offset

        for child in self.children:
            child.add_position(self.position - self.previous_position)
            child.add_scale(self.scale - self.previous_scale)
            child.editor_update(origin_offset)

        self.previous_position = self.position
        self.previous_scale = self.scale
    
    def game_update(self):
        if self.has_script:
            if self.script_has_update == "Untested":
                try: 
                    self.script.update()
                    self.script_has_update = True
                    self.script.ready()
                except:
                    self.script_has_update = False
            elif self.script_has_update:
                self.script.update()
            
            if self.script_has_position == "Untested":
                try: 
                    self.position = self.script.position
                    self.script_has_position = True
                except: 
                    self.script_has_position = False
            elif self.script_has_position:
                self.position = self.script.position
        
        for child in self.children:
            child.add_position(self.position - self.previous_position)
            child.add_scale(self.scale - self.previous_scale)
            child.game_update()
        
        self.previous_position = self.position
    
    def add_position(self, added_position):
        self.position += added_position

        for child in self.children:
            child.add_position(added_position)

    def add_scale(self, added_scale):
        self.scale += added_scale

        for child in self.children:
            child.add_scale(added_scale)
            child.position *= added_scale

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
            "scale_x": self.scale.x,
            "scale_y": self.scale.y,
        }
    
    def load_self(self, node):
        self.script_path = node["script_path"]
        self.position = pygame.Vector2(node["position_x"], node["position_y"])
        self.scale = pygame.Vector2(node["scale_x"], node["scale_y"])
        self.name = node["name"]

        for child in node["children"]:
            if child["type"] == "Position":
                node_to_add = Position()
                node_to_add.load_self(child)
                node_to_add.previous_position = node_to_add.position
                node_to_add.previous_scale = node_to_add.scale
                node_to_add.parent = self
                self.children.append(node_to_add)
            elif child["type"] == "Sprite":
                node_to_add = Sprite()
                node_to_add.load_self(child)
                node_to_add.previous_position = node_to_add.position
                node_to_add.previous_scale = node_to_add.scale
                node_to_add.parent = self
                self.children.append(node_to_add)

class Sprite(Position):
    def __init__(self):
        Position.__init__(self)

        self.sprite_path = None
        self.image = None
        self.node_type = "Sprite"
        self.image_width = None
        self.image_height = None

    def editor_update(self, origin_offset):
        if self.sprite_path:
            raylib.DrawTexturePro(self.image, [0.0, 0.0, self.image_width, self.image_height], [int(self.position.x - self.image_width / 2), int(self.position.y - self.image_height / 2), self.image_width * self.scale.x, self.image_height * self.scale.x], [0, 0], 0.0, raylib.WHITE)

        super().editor_update(origin_offset)

    def game_update(self):
        if self.sprite_path:
            raylib.DrawTexturePro(self.image, [0.0, 0.0, self.image_width, self.image_height], [int(self.position.x - self.image_width / 2), int(self.position.y - self.image_height / 2), self.image_width * self.scale.x, self.image_height * self.scale.x], [0, 0], 0.0, raylib.WHITE)

        super().game_update()

    def set_texture(self, path):
        self.sprite_path = path
        image = raylib.LoadImage(bytes(self.sprite_path, "utf-8"))
        self.image = raylib.LoadTextureFromImage(image)
        self.image_width = image.width
        self.image_height = image.height
        raylib.UnloadImage(image)

    def get_properties_dict(self):
        return {
            "type": "Sprite", 
            "name": self.name,
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x,
            "position_y": self.position.y, 
            "scale_x": self.scale.x,
            "scale_y": self.scale.y,
            "sprite_path": self.sprite_path if self.sprite_path else "None"
        }
    
    def load_self(self, node):
        super().load_self(node)
    
        self.sprite_path = node["sprite_path"] if node["sprite_path"] != "None" else None
        if self.sprite_path:
            self.set_texture(self.sprite_path)

