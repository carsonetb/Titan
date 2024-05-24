import pygame
import raylib
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import json
import copy
import multiprocessing
import os

# Initialise pygame.
pygame.init()

# Initialise raylib.
raylib.SetConfigFlags(raylib.FLAG_WINDOW_RESIZABLE)
raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
raylib.InitWindow(1800, 1000, b"Titan Game Engine")
raylib.SetExitKey(0)

# Load node types
from node_types import Position
from node_types import Sprite
from node_types import Shape
from node_types import PhysicsShape

# Load editor resources.
from resources.button import Button
from resources.list import Hierarchy
from resources.ticker import Ticker
from resources import global_enumerations
import resources.enum
import resources.misc

# Load game runner.
import run_game

# Load fonts.
if os.path.exists("assets/Arimo-VariableFont_wght.ttf"):
    ARIAL_FONT = raylib.LoadFont(b"assets/Arimo-VariableFont_wght.ttf")
else:
    ARIAL_FONT = raylib.LoadFont(os.path.join(os.path.dirname(__file__), "Arimo-VariableFont_wght.ttf").encode("utf-8"))

# [DEPRECATED] Create pygame fonts.
REG_FONT = pygame.font.SysFont("arial", 11)
TITLE_FONT = pygame.font.SysFont("arial", 40)
SUBTITLE_FONT = pygame.font.SysFont("arial", 30)


class AddNodeDialogue:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.position_button = Button(self.x + 10, self.y + 10, self.width - 20, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Position", (0, 0, 0, 255), "arial", 20)
        self.sprite_button = Button(self.x + 10, self.y + 40, self.width - 20, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Sprite", (0, 0, 0, 255), "arial", 20)
        self.shape_button = Button(self.x + 10, self.y + 70, self.width - 20, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Shape", (0, 0, 0, 255), "arial", 20) 
        self.physics_shape_button = Button(self.x + 10, self.y + 100, self.width - 20, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Physics Shape", (0, 0, 0, 255), "arial", 20) 

    def update(self):
        raylib.DrawRectangle(self.x, self.y, self.width, self.height, (170, 170, 170, 255))
        raylib.DrawLine(self.x, self.y, self.x + self.width, self.y, (0, 0, 0, 255))
        raylib.DrawLine(self.x, self.y, self.x, self.y + self.height, (0, 0, 0, 255))
        raylib.DrawLine(self.x + self.width, self.y, self.x + self.width, self.y + self.height, (0, 0, 0, 255))
        raylib.DrawLine(self.x, self.y + self.height, self.x + self.width, self.y + self.height, (0, 0, 0, 255))

        if self.position_button.update() == global_enumerations.BUTTON_JUST_PRESSED: return global_enumerations.NODE_POSITION
        if self.sprite_button.update() == global_enumerations.BUTTON_JUST_PRESSED: return global_enumerations.NODE_SPRITE
        if self.shape_button.update() == global_enumerations.BUTTON_JUST_PRESSED: return global_enumerations.NODE_SHAPE
        if self.physics_shape_button.update() == global_enumerations.BUTTON_JUST_PRESSED: return global_enumerations.NODE_PHYSICS_SHAPE

        if raylib.IsKeyDown(raylib.KEY_ESCAPE):
            return global_enumerations.EXIT


class EditorHandler:
    def __init__(self, project_path):
        self.top_level_nodes = []
        self.background_color = (255, 255, 255, 255)
        self.left_sidebar_width = 300
        self.right_sidebar_width = 330
        self.origin_offset = pygame.Vector2(self.left_sidebar_width, 50)
        self.project_path = project_path
        self.adding_node = False
        self.adding_child = False
        self.node_dialogue = None
        self.selected_node = None
        self.node_hierarchy_display = Hierarchy(30, 50, self.left_sidebar_width - 30)
        self.running_game_process = None

        try:
            project_data_file = open(project_path + "/data.json", "r")
            self.project_data = json.load(project_data_file)
            self.project_data["name"]
            self.project_data["current_scene"]
        except:
            print("WARNING: data.json doesn't exist ... creating.")
            project_data_file = open(project_path + "/data.json", "w")
            project_data_file.write("{\"name\": \"New Titan Project\", \"current_scene\": \"\"}")
            project_data_file.close()

            project_data_file = open(project_path + "/data.json", "r")
            self.project_data = json.load(project_data_file)

        # Node UI specific variables.
        self.shape_type_enum = None
    
    def _draw_engine_sections(self):
        raylib.DrawRectangle(0, 0, raylib.GetScreenWidth(), 50, (180, 180, 180, 255))
        raylib.DrawRectangle(0, 0, self.left_sidebar_width, raylib.GetScreenHeight(), (200, 200, 200, 255))
        raylib.DrawRectangle(raylib.GetScreenWidth() - self.right_sidebar_width, 0, self.right_sidebar_width, raylib.GetScreenHeight(), (200, 200, 200, 255))
        raylib.DrawLine(raylib.GetScreenWidth() - self.right_sidebar_width, 0, raylib.GetScreenWidth() - self.right_sidebar_width, raylib.GetScreenHeight(), (0, 0, 0, 255))
        raylib.DrawLine(self.left_sidebar_width, 0, self.left_sidebar_width, raylib.GetScreenHeight(), (0, 0, 0, 255))
        raylib.DrawLine(0, raylib.GetScreenHeight() - 400, self.left_sidebar_width, raylib.GetScreenHeight() - 400, (0, 0, 0, 255))
        raylib.DrawLine(0, 50, raylib.GetScreenWidth() - self.right_sidebar_width, 50, (0, 0, 0, 255))
        raylib.DrawLine(raylib.GetScreenWidth() - self.right_sidebar_width, 90, raylib.GetScreenWidth(), 90, (0, 0, 0, 255))

    def _draw_engine_constant_buttons(self):
        add_node_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 10, 10, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Add Node", (0, 0, 0, 255), "arial", 20)
        add_node_button_clicked = add_node_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        rename_node_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 170, 50, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Rename Node", (0, 0, 0, 255), "arial", 20)
        rename_node_button_clicked = rename_node_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        add_child_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 170, 10, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Add Child", (0, 0, 0, 255), "arial", 20)
        add_child_button_clicked = add_child_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        delete_node_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 10, 50, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Delete Node", (0, 0, 0, 255), "arial", 20)
        delete_node_button_clicked = delete_node_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        load_scene_button = Button(self.left_sidebar_width + 10, 10, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Load Scene", (0, 0, 0, 255), "arial", 20)
        load_scene_button_clicked = load_scene_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        save_scene_button = Button(self.left_sidebar_width + 170, 10, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Save Scene", (0, 0, 0, 255), "arial", 20)
        save_scene_button_clicked = save_scene_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        if add_node_button_clicked:
            self.adding_node = True
            self.node_dialogue = AddNodeDialogue(200, 200, raylib.GetScreenWidth() - 400, raylib.GetScreenHeight() - 400)

        if rename_node_button_clicked and self.selected_node:
            new_name = tkinter.simpledialog.askstring("Set Name", "New Node Name:")
            if new_name:
                self.selected_node.name = new_name

        if save_scene_button_clicked:
            scene_save_path = tkinter.filedialog.askopenfilename()
            
            if scene_save_path:
                self.save_scene(scene_save_path)

        if add_child_button_clicked and self.selected_node:
            self.adding_node = True
            self.adding_child = True
            self.node_dialogue = AddNodeDialogue(200, 200, raylib.GetScreenWidth() - 400, raylib.GetScreenHeight() - 400)

        if delete_node_button_clicked and self.selected_node:
            if self.selected_node.parent != "Root":
                self.selected_node.parent.children.pop(self.selected_node.parent.children.index(self.selected_node))
            else:
                self.top_level_nodes.pop(self.top_level_nodes.index(self.selected_node))
            
            self.selected_node = None

        if load_scene_button_clicked:
            file_path = tkinter.filedialog.askopenfilename()
            if resources.misc.is_filename_valid(file_path):
                self.load_scene(file_path)
            else:
                print("Warning: Invalid sprite path.")

    def _draw_sprite_specific_options(self, position_addon: pygame.Vector2):
        # Sprite label.
        raylib.DrawTextEx(ARIAL_FONT, "Inherits: Sprite".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 100 + position_addon.y), 30, 3, raylib.BLACK)
        
        mod_texture_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 140 + position_addon.y, 150, 30, 1, 0, (0, 0, 0, 255), (255, 255, 255, 0), b"Attach Texture" if not self.selected_node.sprite_path else b"Remove Texture", (0, 0, 0, 255), "arial", 20)
        
        if mod_texture_button.update() == global_enumerations.BUTTON_JUST_PRESSED:
            self.selected_node.set_texture(tkinter.filedialog.askopenfilename())

        self._draw_position_specific_options(pygame.Vector2(position_addon.x, position_addon.y + 80))
    
    def _draw_shape_specific_options(self, position_addon: pygame.Vector2):
        # Shape label.
        raylib.DrawTextEx(ARIAL_FONT, "Inherits: Shape".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 100 + position_addon.y), 30, 3, raylib.BLACK)

        # Color button.
        change_color_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y, 150, 30, 1, 0, raylib.BLACK, raylib.WHITE, b"Change Color", raylib.BLACK, "loller", 20)

        # Update color button.
        changing_color = change_color_button.update() == global_enumerations.BUTTON_JUST_PRESSED

        if changing_color:
            # Needs a bunch of code for a dialogue that changes the color.
            pass 

        dynamic_position_addon_y = 120

        if self.selected_node.shape_index == global_enumerations.SHAPE_RECT:
            # Width/height tickers.
            mod_width_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y + 40, 150, 30, 0, 20, self.selected_node.width, 5)
            mod_height_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 220 + position_addon.y + 40, 150, 30, 0, 20, self.selected_node.height, 5)

            # Width/height labels.
            raylib.DrawTextEx(ARIAL_FONT, "Width".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 180 + position_addon.y + 40), 30, 3, raylib.BLACK)
            raylib.DrawTextEx(ARIAL_FONT, "Height".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 220 + position_addon.y + 40), 30, 3, raylib.BLACK)

            # Update tickers.
            mod_width_ticker.update()
            mod_height_ticker.update()

            # Modify values changed by tickers.
            self.selected_node.width = mod_width_ticker.value
            self.selected_node.height = mod_height_ticker.value

            dynamic_position_addon_y += 80

        if self.selected_node.shape_index == global_enumerations.SHAPE_CIRCLE:
            # Radius ticker.
            mod_radius_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y + 40, 150, 30, 0, 20, self.selected_node.radius, 5)

            # Radius labels.
            raylib.DrawTextEx(ARIAL_FONT, "Radius".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 180 + position_addon.y + 40), 30, 3, raylib.BLACK)

            # Update ticker.
            mod_radius_ticker.update()

            # Modify value changed by ticker.
            self.selected_node.radius = mod_radius_ticker.value

            dynamic_position_addon_y += 40

        if self.selected_node.shape_index == global_enumerations.SHAPE_POLYGON or self.selected_node.shape_index == global_enumerations.SHAPE_LINE:
            # Button for adding a point.
            add_point_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 180 + position_addon.y, 150, 30, 1, 0, raylib.BLACK, raylib.WHITE, b"Add Point", raylib.BLACK, "skib", 20)

            if add_point_button.update() == global_enumerations.BUTTON_JUST_PRESSED:
                self.selected_node.points_real_positions.append((0, 0))
                self.selected_node.points.append((0, 0))
            
            # Create position tickers.
            position_tickers = []

            for i in range(len(self.selected_node.points)):
                position_tickers.append(Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y + 40 + i * 80, 150, 30, 0, 20, self.selected_node.points_real_positions[i][0], 5))
                position_tickers.append(Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 220 + position_addon.y + 40 + i * 80, 150, 30, 0, 20, self.selected_node.points_real_positions[i][1], 5))

            # Draw position labels.
            for i in range(len(self.selected_node.points)):
                raylib.DrawTextEx(ARIAL_FONT, f"Position {i} X".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 180 + position_addon.y + 40 + i * 80), 25, 3, raylib.BLACK)
                raylib.DrawTextEx(ARIAL_FONT, f"Position {i} Y".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 220 + position_addon.y + 40 + i * 80), 25, 3, raylib.BLACK)

            # Update position tickers.
            for ticker in position_tickers:
                ticker.update()

            # Modify values changed by tickers.
            for i in range(len(position_tickers)):
                if i % 2 == 0:
                    self.selected_node.points_real_positions[i // 2] = (position_tickers[i].value, self.selected_node.points_real_positions[i // 2][1])
                else:
                    self.selected_node.points_real_positions[i // 2] = (self.selected_node.points_real_positions[i // 2][0], position_tickers[i].value)

            self.selected_node.update_polygon_points(self.selected_node.points_real_positions)

            dynamic_position_addon_y += len(position_tickers) * 40

        # Enumeration for shape type.
        if not self.shape_type_enum:
            self.shape_type_enum = resources.enum.EnumSelectionMenu({
                "Rectangle": global_enumerations.SHAPE_RECT,
                "Circle": global_enumerations.SHAPE_CIRCLE,
                "Line": global_enumerations.SHAPE_LINE,
                "Polygon": global_enumerations.SHAPE_POLYGON, 
            }, "Rectangle", raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 140 + position_addon.y, 150, 30, 0, 20)

        self.shape_type_enum.position.x = raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x

        updated_shape_type = self.shape_type_enum.update()
        if updated_shape_type:
            self.selected_node.shape_index = self.shape_type_enum.enum.enum[self.shape_type_enum.enum.item_selected]

        self._draw_position_specific_options(pygame.Vector2(position_addon.x, dynamic_position_addon_y + position_addon.y))

    def _draw_physics_shape_specific_options(self, position_addon: pygame.Vector2):
        # Shape label.
        raylib.DrawTextEx(ARIAL_FONT, "Inherits: Physics Shape".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 100 + position_addon.y), 28, 3, raylib.BLACK)

        # Velocity tickers.
        mod_velocity_x_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 140 + position_addon.y, 150, 30, 0, 20, self.selected_node.velocity.x)
        mod_velocity_y_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y, 150, 30, 0, 20, self.selected_node.velocity.y)

        # Update tickers.
        mod_velocity_x_ticker.update()
        mod_velocity_y_ticker.update()

        # Set velocity values.
        self.selected_node.velocity.x = mod_velocity_x_ticker.value
        self.selected_node.velocity.y = mod_velocity_y_ticker.value

        self._draw_shape_specific_options(pygame.Vector2(position_addon.x, 120 + position_addon.y))

    def _draw_position_specific_options(self, position_addon: pygame.Vector2):
        # Position label.
        raylib.DrawTextEx(ARIAL_FONT, "Inherits: Position".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 100 + position_addon.y), 30, 3, raylib.BLACK)

        # Position tickers.
        mod_position_x_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 140 + position_addon.y, 150, 30, 0, 20, self.selected_node.position.x)
        mod_position_y_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 180 + position_addon.y, 150, 30, 0, 20, self.selected_node.position.y)

        # Scale tickers.
        mod_scale_x_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 240 + position_addon.y, 150, 30, 0, 20, self.selected_node.scale.x, 0.1)
        mod_scale_y_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 280 + position_addon.y, 150, 30, 0, 20, self.selected_node.scale.y, 0.1)

        # Rotation ticker.
        mod_rotation_ticker = Ticker(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 340 + position_addon.y, 150, 30, 0, 20, self.selected_node.rotation_degrees, 1)

        # Position labels.
        raylib.DrawTextEx(ARIAL_FONT, "Position X".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 140 + position_addon.y), 30, 3, raylib.BLACK)
        raylib.DrawTextEx(ARIAL_FONT, "Position Y".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 180 + position_addon.y), 30, 3, raylib.BLACK)

        # Scale labels.
        raylib.DrawTextEx(ARIAL_FONT, "Scale X".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 240 + position_addon.y), 30, 3, raylib.BLACK)
        raylib.DrawTextEx(ARIAL_FONT, "Scale Y".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 280 + position_addon.y), 30, 3, raylib.BLACK)

        # Rotation label.
        raylib.DrawTextEx(ARIAL_FONT, "Rotation".encode("ascii"), (raylib.GetScreenWidth() - self.right_sidebar_width + 170 + position_addon.x, 340 + position_addon.y), 30, 3, raylib.BLACK)

        # Attach script button.
        attach_script_button = Button(raylib.GetScreenWidth() - self.right_sidebar_width + 10 + position_addon.x, 400 + position_addon.y, 200, 30, 1, 0, raylib.BLACK, raylib.WHITE, b"Attach Script" if not self.selected_node.script else b"Detach Script", raylib.BLACK, "", 30)

        # Update tickers.
        mod_position_x_ticker.update()
        mod_position_y_ticker.update()
        mod_scale_x_ticker.update()
        mod_scale_y_ticker.update()
        mod_rotation_ticker.update()

        # Update buttons.
        attach_script_button_pressed = attach_script_button.update()

        if attach_script_button_pressed == global_enumerations.BUTTON_JUST_PRESSED:
            if self.selected_node.script:
                self.selected_node.script = None
                self.selected_node.script_path = ""
            else:
                script_file_path = tkinter.filedialog.askopenfilename()

                # Attach a script to the node if the path is valid.
                if resources.misc.is_filename_valid(script_file_path):
                    self.selected_node.load_script(script_file_path)

        # Modify values changed by tickers.
        self.selected_node.add_position(pygame.Vector2(mod_position_x_ticker.value - self.selected_node.position.x, mod_position_y_ticker.value - self.selected_node.position.y))
        self.selected_node.add_scale(pygame.Vector2(mod_scale_x_ticker.value - self.selected_node.scale.x, mod_scale_y_ticker.value - self.selected_node.scale.y))
        self.selected_node.add_rotation(resources.misc.deg_to_rad(mod_rotation_ticker.value) - self.selected_node.rotation)

    def _update_add_node_dialogue(self):
        self.node_to_add = self.node_dialogue.update()

        if self.node_to_add:
            if self.node_to_add == global_enumerations.NODE_POSITION: child = Position()
            if self.node_to_add == global_enumerations.NODE_SPRITE: child = Sprite()
            if self.node_to_add == global_enumerations.NODE_SHAPE: child = Shape()
            if self.node_to_add == global_enumerations.NODE_PHYSICS_SHAPE: child = PhysicsShape()
            if self.node_to_add == global_enumerations.EXIT:
                self.adding_node = False
                self.adding_child = False
                self.node_dialogue = False
                return
                
            if self.adding_child and self.selected_node: 
                child.parent = self.selected_node
                child.position = child.parent.position
                child.scale = child.parent.scale
                child.rotation = child.parent.rotation
                self.selected_node.children.append(child)
            else: 
                self.top_level_nodes.append(child)

            self.adding_node = False
            self.adding_child = False
            self.node_dialogue = None

    def _get_nodes_hierarchy(self):
        nodes = []

        for node in self.top_level_nodes:
            nodes.append(node.get_children_recursive())
        
        return nodes

    def _draw_play_stop_buttons(self):
        # Define width and height values
        box_width = 70
        box_height = 30

        # Draw defining rectangle.
        raylib.DrawRectangleRoundedLines((raylib.GetScreenWidth() / 2 - box_width / 2, 10, box_width, box_height), 0.5, 1, 2, raylib.BLACK)

        # Create play and stop buttons.
        play_button = Button(raylib.GetScreenWidth() / 2 - box_width / 2 + 10, 15, 20, 20, 1, 0, raylib.BLACK, raylib.WHITE, b"/\\", raylib.BLACK, "", 20)
        stop_button = Button(raylib.GetScreenWidth() / 2 - box_width / 2 + 40, 15, 20, 20, 1, 0, raylib.BLACK, raylib.WHITE, b"[]", raylib.BLACK, "", 20)

        # Update buttons.
        play_button_pressed = play_button.update()
        stop_button_pressed = stop_button.update()

        # Start the game in another thread if the play button is pressed.
        if play_button_pressed == global_enumerations.BUTTON_JUST_PRESSED:
            # Save scene before starting.
            print("INFO: Saving scene before running game.")
            project_data_file = open(self.project_path + "/data.json", "r")
            self.project_data = json.load(project_data_file)
            self.save_scene(self.project_data["current_scene"])

            print("INFO: Starting game running subprocess.")
            self.running_game_process = multiprocessing.Process(target=run_game.running_game_process, args=(self.project_path,))
            self.running_game_process.start()

        if stop_button_pressed == global_enumerations.BUTTON_JUST_PRESSED and self.running_game_process:
            print("INFO: Stopping game running subprocess.")
            self.running_game_process.terminate()

    def update(self):
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.RAYWHITE)

        # IMPORTANT: Update all nodes!
        for node in self.top_level_nodes:
            node.editor_update(self.origin_offset)
        
        # Set selected_node variable.
        if self.node_hierarchy_display.selected_item:
            self.selected_node = self.node_hierarchy_display.selected_item

        # Get nodes hierarchy.
        nodes = self._get_nodes_hierarchy()

        # Draw engine section lines and rectangles.
        self._draw_engine_sections()

        # Draw buttons located in the top right corner of the screen.
        self._draw_engine_constant_buttons()

        # Draw play buttons.
        self._draw_play_stop_buttons()

        # Draw project title.
        raylib.DrawTextEx(ARIAL_FONT, bytes(self.project_data["name"], 'utf-8'), (10, 10), 30, 3, (0, 0, 0, 255))

        # Draw dedicated menu items for selected object.
        if self.selected_node:
            if self.selected_node.node_type == "Position":
                self._draw_position_specific_options(pygame.Vector2(0, 0))
            if self.selected_node.node_type == "Sprite":
                self._draw_sprite_specific_options(pygame.Vector2(0, 0))
            if self.selected_node.node_type == "Shape":
                self._draw_shape_specific_options(pygame.Vector2(0, 0))
            if self.selected_node.node_type == "PhysicsShape":
                self._draw_physics_shape_specific_options(pygame.Vector2(0, 0))

        # Handle adding new node if we're doing that.
        if self.adding_node:
            self._update_add_node_dialogue()

        # Update node hierarchy display.
        self.node_hierarchy_display.items = nodes
        self.node_hierarchy_display.recurse_draw_list(nodes, 0, 0)

        # Draw debug FPS in the bottom left corner.
        raylib.DrawFPS(10, raylib.GetScreenHeight() - 30)

        raylib.EndDrawing()

    def load_scene(self, filename, save_scene=True):
        # Save scene before loading another one.
        if save_scene:
            save_scene_path = json.load(open(self.project_path + "/data.json", "r"))["current_scene"]        
            self.save_scene(save_scene_path)

        # Load scene file.
        scene_file = open(filename, "r")
        data = json.load(scene_file)

        # Clear nodes.
        self.top_level_nodes = []

        # Set the previously opened scene.
        project_global_data_file = open(self.project_path + "/data.json", "r")
        project_global_data = json.load(project_global_data_file)
        project_global_data["current_scene"] = filename
        project_global_data_file.close()

        # Write to data file.
        project_global_data_file = open(self.project_path + "/data.json", "w")
        project_global_data_file.write(str(project_global_data).replace("'", '"'))

        # Loop through top level nodes and add them in ...
        # nodes will add their own children.
        for node in data:
            if node["type"] == "Position":
                node_to_add = Position()
            elif node["type"] == "Sprite":
                node_to_add = Sprite()
            elif node["type"] == "Shape":
                node_to_add = Shape()
            elif node["type"] == "PhysicsShape":
                node_to_add = PhysicsShape()

            # Nodes loads itself ... will add it's children.
            node_to_add.load_self(node)

            # Set previous position of nodes because that isn't saved.
            node_to_add.previous_position = node_to_add.position
            node_to_add.previous_scale = node_to_add.scale
            self.top_level_nodes.append(node_to_add)

    # Save scene at path.
    def save_scene(self, scene_save_path):
        scene_save_file = open(scene_save_path, "w+")
        scene_save_file.write(str([self.top_level_nodes[i].get_properties_dict() for i in range(len(self.top_level_nodes))]).replace("'", '"'))
        scene_save_file.close()

class TitanMainMenu:
    def __init__(self, local_data_path):
        self.running_project = False
        self.editor_container = None
        self.local_data_path = local_data_path

    def prepare_for_close(self):
        print("WARNING: Unprecedented close detected!")

        if self.editor_container:
            save_scene_path = json.load(open(self.editor_container.project_path + "/data.json", "r"))["current_scene"]        
            
            if save_scene_path:
                self.editor_container.save_scene(save_scene_path)
    
    def update(self):
        self.add_project_button = Button(10, 10, 150, 50, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Add Project", (0, 0, 0, 255), b"assets/Arimo-VariableFont_wght.ttf", 20)
        self.open_project_button = Button(0, 0, 200, 50, 1, 0, (0, 0, 0, 255), (255, 255, 255, 255), b"Open Project", (0, 0, 0, 255), b"assets/Arimo-VariableFont_wght.ttf", 20)
        
        if not self.running_project:
            raylib.BeginDrawing()
            raylib.ClearBackground(raylib.RAYWHITE)

            try:
                project_list_file = open(self.local_data_path + "/projects.json", "r")
            except:
                print("ERROR: Global project list file does not exist in directory ... creating project list file.")

                project_list_file = open(self.local_data_path + "/projects.json", "x")
                project_list_file.write("[]")
                project_list_file.close()

                return

            try:
                projects = json.load(project_list_file)
            except Exception as error_message:
                print("ERROR: Failed to parse global project list json file (although file exists). Dumping json parse error ...")
                print(error_message)
                print("Clearing global project list ...")

                project_list_file = open(self.local_data_path + "/projects.json", "w")
                project_list_file.write("[]")
                project_list_file.close()

                return
                
            button_pressed = self.add_project_button.update() == global_enumerations.BUTTON_JUST_PRESSED

            if button_pressed:
                project_path = tkinter.filedialog.askdirectory()
                
                if not project_path in projects:
                    projects.append(project_path)

                    project_list_file.close()

                    project_list_file_w = open(self.local_data_path + "/projects.json", "w")
                    project_list_file_w.write(str(projects).replace("'", '"'))
                    project_list_file_w.close()

                    try:
                        project_data_file = open(project_path + "/data.json", "x")
                        project_data_file.write("{\"project_name\": \"New Titan Project\", \"current_scene\": \"\"}")
                    except:
                        print("WARNING: Project exists. Proceding.")

            for i in range(len(projects)):
                raylib.DrawTextEx(ARIAL_FONT, bytes(projects[i], 'utf-8'), (10, 200 + i * 100), 30, 3, (0, 0, 0, 255))
                button = copy.copy(self.open_project_button)
                button.x = raylib.GetScreenWidth() - button.width - 10
                button.y = 200 + i * 100 - 5
                start_proj_clicked = button.update() == global_enumerations.BUTTON_JUST_PRESSED
                raylib.DrawLine(0, 200 + i * 100 - 30, raylib.GetScreenWidth(), 200 + i * 100 - 30, (0, 0, 0, 255))
                raylib.DrawLine(0, 200 + i * 100 + 70, raylib.GetScreenWidth(), 200 + i * 100 + 70, (0, 0, 0, 255))

                if start_proj_clicked:
                    self.running_project = True
                    self.editor_container = EditorHandler(projects[i])

                    # If current scene exists, load it automatically.
                    with open(projects[i] + "/data.json") as project_file:
                        project_data = json.load(project_file)

                        if project_data["current_scene"] != "":
                            self.editor_container.load_scene(project_data["current_scene"], save_scene=False)

                    return
                
            raylib.DrawFPS(10, 10)
                
            raylib.EndDrawing()
        
        else:
            return self.editor_container.update() == global_enumerations.BUTTON_JUST_PRESSED

