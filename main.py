import pygame
import importlib
import sys
from node_types.position import Position
from node_types.sprite import Sprite
from resources.button import Button
from resources.list import Hierarchy
from pygame import gfxdraw
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import json
import copy

pygame.init()
pygame.font.init()

REG_FONT = pygame.font.SysFont("arial", 11)
TITLE_FONT = pygame.font.SysFont("arial", 40)
SUBTITLE_FONT = pygame.font.SysFont("arial", 30)


class AddNodeDialogue:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.position_button = Button(self.x + 10, self.y + 10, self.width - 20, 30, 1, 0, (0, 0, 0), (255, 255, 255), "Position", (0, 0, 0), "arial", 20)
        self.sprite_button = Button(self.x + 10, self.y + 40, self.width - 20, 30, 1, 0, (0, 0, 0), (255, 255, 255), "Sprite", (0, 0, 0), "arial", 20)
    
    def update(self, window):
        pygame.draw.rect(window, (170, 170, 170), (self.x, self.y, self.width, self.height))
        pygame.draw.line(window, (0, 0, 0), (self.x, self.y), (self.x + self.width, self.y))
        pygame.draw.line(window, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height))
        pygame.draw.line(window, (0, 0, 0), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        pygame.draw.line(window, (0, 0, 0), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height))

        if self.position_button.update(window): return "Position"
        if self.sprite_button.update(window): return "Sprite"


class EditorHandler:
    def __init__(self, window, project_path):
        self.window = window
        self.top_level_nodes = []
        self.background_color = pygame.Vector3(255, 255, 255)
        self.left_sidebar_width = 300
        self.right_sidebar_width = 300
        self.origin_offset = pygame.Vector2(self.left_sidebar_width, 0)
        self.project_path = project_path
        self.adding_node = False
        self.node_dialogue = None
        self.selected_node = None
        self.node_hierarchy_display = Hierarchy(30, 50, self.left_sidebar_width - 30)

        project_data_file = open(project_path + "/data.json", "r")
        self.project_data = json.load(project_data_file)
        
        self.project_name_text = SUBTITLE_FONT.render(self.project_data["name"], True, (0, 0, 0))

    def update(self):
        self.window.fill(self.background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 800:
                    width = 800
                if height < 800:
                    height = 800
                self.window = pygame.display.set_mode((width,height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

        for node in self.top_level_nodes:
            node.editor_update(self.window, self.origin_offset)

        pygame.draw.rect(self.window, (200, 200, 200), (0, 0, self.left_sidebar_width, self.window.get_height()))
        pygame.draw.rect(self.window, (200, 200, 200), (self.window.get_width() - self.right_sidebar_width, 0, self.right_sidebar_width, self.window.get_height()))
        gfxdraw.line(self.window, self.window.get_width() - self.right_sidebar_width, 0, self.window.get_width() - self.right_sidebar_width, self.window.get_height(), (0, 0, 0))
        gfxdraw.line(self.window, self.left_sidebar_width, 0, self.left_sidebar_width, self.window.get_height(), (0, 0, 0))
        gfxdraw.line(self.window, 0, self.window.get_height() - 400, self.left_sidebar_width, self.window.get_height() - 400, (0, 0, 0))
        gfxdraw.line(self.window, 0, 50, self.left_sidebar_width, 50, (0, 0, 0))

        self.window.blit(self.project_name_text, (10, 10))

        add_node_button = Button(self.window.get_width() - self.right_sidebar_width + 10, 10, 150, 50, 1, 0, (0, 0, 0), (255, 255, 255), "Add Node", (0, 0, 0), "arial", 20)
        add_node_button_clicked = add_node_button.update(self.window)

        rename_node_button = Button(self.window.get_width() - self.right_sidebar_width + 170, 10, 150, 50, 1, 0, (0, 0, 0), (255, 255, 255), "Rename Node", (0, 0, 0), "arial", 20)
        rename_node_button_clicked = rename_node_button.update(self.window)

        if add_node_button_clicked:
            self.adding_node = True
            self.node_dialogue = AddNodeDialogue(200, 200, self.window.get_width() - 400, self.window.get_height() - 400)

        if rename_node_button_clicked and self.node_hierarchy_display.selected_item:
            new_name = tkinter.simpledialog.askstring("Set Name", "New Node Name:")
            if new_name:
                self.node_hierarchy_display.selected_item.name = new_name
        
        if self.adding_node:
            self.node_to_add = self.node_dialogue.update(self.window)

            if self.node_to_add:
                if self.node_to_add == "Position":
                    self.top_level_nodes.append(Position())

                self.adding_node = False
                self.node_dialogue = None

        nodes = []

        for node in self.top_level_nodes:
            nodes.append(node.get_children_recursive())

        self.node_hierarchy_display.items = nodes
        self.node_hierarchy_display.recurse_draw_list(self.window, nodes, 0, 0)

        pygame.display.update()


class TitanMainMenu:
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.add_project_button = Button(10, 10, 150, 50, 1, 0, (0, 0, 0), (255, 255, 255), "Add Project", (0, 0, 0), "Arial", 20)
        self.open_project_button = Button(0, 0, 200, 50, 1, 0, (0, 0, 0), (255, 255, 255), "Open Project", (0, 0, 0), "Arial", 20)
        self.running_project = False
        self.editor_container = None
    
    def update(self):
        if not self.running_project:
            self.window.fill((200, 200, 200))

            project_list_file = open("projects.json")
            projects = json.load(project_list_file)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1
                
            button_pressed = self.add_project_button.update(self.window)

            if button_pressed:
                project_path = tkinter.filedialog.askdirectory()
                
                if not project_path in projects:
                    projects.append(project_path)

                    project_list_file.close()

                    project_list_file_w = open("projects.json", "w")
                    project_list_file_w.write(str(projects).replace("'", '"'))
                    project_list_file_w.close()

                    project_data_file = open(project_path + "/data.json", "x")
                    project_data_file.write("{\"project_name\": \"New Titan Project}")

            for i in range(len(projects)):
                project_name = SUBTITLE_FONT.render(projects[i], True, (0, 0, 0))
                self.window.blit(project_name, (10, 200 + i * 100))
                button = copy.copy(self.open_project_button)
                button.x = self.window.get_width() - button.width - 10
                button.y = 200 + i * 100 - 5
                start_proj_clicked = button.update(self.window)
                pygame.draw.line(self.window, (0, 0, 0), (0, 200 + i * 100 - 30), (self.window.get_width(), 200 + i * 100 - 30))
                pygame.draw.line(self.window, (0, 0, 0), (0, 200 + i * 100 + 70), (self.window.get_width(), 200 + i * 100 + 70))

                if start_proj_clicked:
                    self.running_project = True
                    self.editor_container = EditorHandler(self.window, projects[i])
                    return
                
            pygame.display.update()
        
        else:
            return self.editor_container.update()


def main():
    # Initialize Main Menu
    main_menu = TitanMainMenu(1800, 1000)

    while True:
        action_code = main_menu.update()

        if action_code == 1:
            break
    

if __name__ == "__main__":
    main()