import pymunk.pygame_util
import raylib
import json
import pymunk

# Load node types
from node_types.position import Position
from node_types.sprite import Sprite
from node_types.shape import Shape
from node_types.physics_shape import PhysicsShape
from node_types.rigid_body import RigidBody
from node_types.static_body import StaticBody
from node_types.kinematic_body import KinematicBody

# Run game dependencies.
from resources.misc import global_enumerations

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
        elif node["type"] == "PhysicsShape":
            node_to_add = PhysicsShape()
        elif node["type"] == "RigidBody":
            node_to_add = RigidBody()
        elif node["type"] == "StaticBody":
            node_to_add = StaticBody()
        elif node["type"] == "KinematicBody":
            node_to_add = KinematicBody()

        # Nodes loads itself ... will add it's children.
        node_to_add.load_self(node)

        # Set previous position of nodes because that isn't saved.
        node_to_add.previous_position = node_to_add.position
        node_to_add.previous_scale = node_to_add.scale
        top_level_nodes.append(node_to_add)

    return top_level_nodes

def debug_scene_hierarchy(top_level_nodes, layers=0):
    for node in top_level_nodes:
        print("\t" * layers + node.name)
        debug_scene_hierarchy(node.children, layers + 1)

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
    raylib.InitWindow(1170, 950, (project_data["name"] + " (DEBUG)").encode("ascii"))
    raylib.SetExitKey(0)
    raylib.SetTargetFPS(60)

    # Create physics space.
    physics_space = pymunk.Space(True)
    physics_space.gravity = (0, 981)
    physics_space.collision_bias = 0.5

    # pygame.init()
    # screen = pygame.display.set_mode((1000, 700))
    # draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Initialize default scene.
    top_level_nodes = load_scene(project_data["current_scene"], project_path)

    # Running game mainloop.
    while not raylib.WindowShouldClose():
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.RAYWHITE)
        
        # IMPORTANT: Update all nodes!
        for node in top_level_nodes:
            if node.node_type == "RigidBody" or node.node_type == "StaticBody" or node.node_type == "KinematicBody":
                node.game_update(physics_space)
            else:
                node.game_update()
        
        # Step physics simulation.
        physics_space.step(1/60)
        
        # screen.fill(pygame.Color("white"))
        # physics_space.debug_draw(draw_options)
        # pygame.display.flip()
            
        # Draw debug FPS in the top left corner.
        raylib.DrawFPS(10, 10)

        raylib.EndDrawing()

    raylib.CloseWindow()