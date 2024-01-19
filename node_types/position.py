import pygame
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
    
    def editor_update(self, window, origin_offset):
        offset_position = origin_offset + self.position
        gfxdraw.circle(window, int(offset_position.x), int(offset_position.y), 15, (0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

        if self.selected and offset_position.distance_to(mouse_pos) < 30:
            pygame.draw.circle(window, (0, 0, 0), offset_position, 15)

            if pygame.mouse.get_pressed()[0]:
                self.mouse_dragging = True
            else:
                self.mouse_dragging = False
        
        if self.mouse_dragging:
            self.position = mouse_pos - origin_offset

        for child in self.children:
            child.add_position(self.position - self.previous_position)
            child.editor_update(window, origin_offset)

        self.previous_position = self.position
    
    def game_update(self, window):
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
            child.game_update(window)
        
        self.previous_position = self.position

    def get_children_recursive(self):
        children = [self]

        for child in self.children:
            children.append(child.get_children_recursive())

        return children
    
    def add_position(self, added_position):
        self.position += added_position

        for child in self.children:
            child.add_position(added_position)

    def get_properties_dict(self):
        return {
            "type": "Position", 
            "name": self.name,
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x, 
            "position_y": self.position.y
        }
    
    def load_self(self, node):
        self.script_path = node["script_path"]
        self.position = pygame.Vector2(node["position_x"], node["position_y"])
        self.name = node["name"]

        for child in node["children"]:
            if child["type"] == "Position":
                node = Position()
                node.load_self(child)
                node.previous_position = node.position
                node.parent = self
                self.children.append(node)
