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

        if offset_position.distance_to(mouse_pos) < 30:
            pygame.draw.circle(window, (0, 0, 0), offset_position, 15)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_dragging = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_dragging = False
        
        if self.mouse_dragging:
            self.position = mouse_pos - origin_offset

        for child in self.children:
            child.editor_update(window, origin_offset)
            child.position += self.position - self.previous_position

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
            child.game_update(window)
            child.position += self.position - self.previous_position
        
        self.previous_position = self.position

    def get_children_recursive(self):
        children = [self]

        for child in self.children:
            children += child.get_children_recursive()

        return children