import pygame
import importlib
import sys
from node_types.position import Position
from node_types.sprite import Sprite
from resources.button import Button
from pygame import gfxdraw
import tkinter
import tkinter.filedialog
import json

pygame.init()
pygame.font.init()

REG_FONT = pygame.font.SysFont("arial", 32)


class EditorHandler:
    def __init__(self, window):
        self.window = window
        self.top_level_nodes = []
        self.background_color = pygame.Vector3(255, 255, 255)
        self.left_sidebar_width = 300
        self.origin_offset = pygame.Vector2(self.left_sidebar_width, 0)

    def update(self):
        self.window.fill(self.background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

        for node in self.top_level_nodes:
            node.editor_update(self.window, self.origin_offset)

        pygame.draw.rect(self.window, (200, 200, 200), (0, 0, self.left_sidebar_width, self.window.get_height()))
        gfxdraw.line(self.window, self.left_sidebar_width, 0, self.left_sidebar_width, self.window.get_height(), (0, 0, 0))

        nodes = []

        for node in self.top_level_nodes:
            nodes += node.get_children_recursive()

        for i in range(len(nodes)):
            node_text = REG_FONT.render(nodes[i].name, True, (0, 0, 0))
            self.window.blit(node_text, (10, 10 + i * 30))

        pygame.display.update()


class TitanMainMenu:
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.add_project_button = Button(10, 10, 150, 50, 2, 5, (0, 0, 0), (255, 255, 255), "Add Project", (0, 0, 0), "Arial", 20)
    
    def update(self):
        self.window.fill((200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            
        button_pressed = self.add_project_button.update(self.window)

        if button_pressed:
            project_path = tkinter.filedialog.askdirectory()
            
        pygame.display.update()


def main():
    # Initialize Main Menu
    main_menu = TitanMainMenu(1800, 1000)

    while True:
        action_code = main_menu.update()

        if action_code == 1:
            break
    

if __name__ == "__main__":
    main()