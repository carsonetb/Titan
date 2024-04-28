import pygame
import raylib
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import json
import copy
import multiprocessing

# Initialise pygame.
pygame.init()

# Load node types
from node_types import Position
from node_types import Sprite
from node_types import Shape

# Run game dependencies.
from resources import global_enumerations

def load_scene(filename, project_path):
    # Load scene file.
    scene_file = open(filename, "r")
    data = json.load(scene_file)

    # Clear nodes.
    top_level_nodes = []

    # Set the previously opened scene.
    project_global_data_file = open(project_path + "/data.json", "r")
    project_global_data = json.load(project_global_data_file)
    project_global_data["current_scene"] = filename
    project_global_data_file.close()

    # Write to data file.
    project_global_data_file = open(project_path + "/data.json", "w")
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

        # Nodes loads itself ... will add it's children.
        node_to_add.load_self(node)

        # Set previous position of nodes because that isn't saved.
        node_to_add.previous_position = node_to_add.position
        node_to_add.previous_scale = node_to_add.scale
        top_level_nodes.append(node_to_add)

    return top_level_nodes

def running_game_process(project_path):
    # Load project data file.
    try:
        project_data_file = open(project_path + "/data.json", "r")
        project_data = json.load(project_data_file)
        project_data["name"]
        project_data["current_scene"]
    except:
        print("ERROR: Attempt to run corrupt/nonexistant game. Aborting.")
        return global_enumerations.EXIT_ERRORS_FATAL
    
    # Close ghost window.
    raylib.CloseWindow()
    
    # Initialise raylib.
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_RESIZABLE)
    raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
    raylib.InitWindow(1000, 800, project_data["name"].encode("ascii"))
    raylib.SetExitKey(0)

    # Initialize default scene.
    top_level_nodes = load_scene(project_data["current_scene"], project_path)

    # Running game mainloop.
    while not raylib.WindowShouldClose():
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.RAYWHITE)
        
        # IMPORTANT: Update all nodes!
        for node in top_level_nodes:
            node.game_update()
            
        # Draw debug FPS in the top left corner.
        raylib.DrawFPS(10, 10)

        raylib.EndDrawing()

    raylib.CloseWindow()