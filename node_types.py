import pygame
import raylib
import importlib
import sys
import tripy
import numpy

import resources.misc
from resources import global_enumerations
from resources.button import Button
from resources.button import InvisibleButton

class Position:
    def __init__(self):
        self.script_path = ""
        self.script = None
        self.node_type = "Position"
        self.position = pygame.Vector2(0, 0)
        self.previous_position = pygame.Vector2(0, 0)
        self.scale = pygame.Vector2(1, 1)
        self.previous_scale = pygame.Vector2(1, 1)
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
    
    def editor_update(self, origin_offset):
        offset_position = origin_offset + self.position
        raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 15, (0, 0, 0, 255))
        
        if self.selected:
            raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), 18, (0, 0, 0, 255))

        mouse_pos = raylib.GetMousePosition()
        mouse_pos = pygame.Vector2(mouse_pos.x, mouse_pos.y)

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
            self.position = mouse_pos - origin_offset

        for child in self.children:
            child.add_position(self.position - self.previous_position)
            child.add_scale(self.scale - self.previous_scale)
            child.editor_update(origin_offset)

        if self.position != self.previous_position:
            self.just_moved = True
        else:
            self.just_moved = False

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
        self.previous_scale = self.scale
    
    def add_position(self, added_position):
        self.position += added_position

        for child in self.children:
            child.add_position(added_position)

    def add_scale(self, added_scale: pygame.Vector2):
        if added_scale == pygame.Vector2(0, 0):
            return

        self.scale += added_scale

        for child in self.children:
            child.add_scale(added_scale)
            child.position += pygame.Vector2((child.position - self.position).x * added_scale.x, (child.position - self.position).y * added_scale.y)

    def add_rotation(self, added_rotation: float):
        self.rotation += added_rotation
        self.rotation_degrees = resources.misc.rad_to_deg(self.rotation)

        for child in self.children:
            position_to_rotate = child.position - self.position
            rotated_position = position_to_rotate.rotate_rad(added_rotation)
            child.position = self.position + rotated_position
            child.add_rotation(added_rotation)

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
    
    def load_self(self, node):
        self.script_path = node["script_path"]
        self.position = pygame.Vector2(node["position_x"], node["position_y"])
        self.scale = pygame.Vector2(node["scale_x"], node["scale_y"])
        self.rotation = node["rotation"]
        self.rotation_degrees = resources.misc.rad_to_deg(self.rotation)
        
        self.name = node["name"]

        for child in node["children"]:
            if child["type"] == "Position":
                node_to_add = Position()
            elif child["type"] == "Sprite":
                node_to_add = Sprite()
            elif child["type"] == "Shape":
                node_to_add = Shape()

            node_to_add.load_self(child)
            node_to_add.previous_position = node_to_add.position
            node_to_add.previous_scale = node_to_add.scale
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
        offset_position = self.position + origin_offset

        if self.sprite_path:
            raylib.DrawTexturePro(self.image, [0.0, 0.0, self.image_width, self.image_height], [int(offset_position.x - (self.image_width * self.scale.x) / 2), int(offset_position.y - (self.image_height * self.scale.y) / 2), self.image_width * self.scale.x, self.image_height * self.scale.y], [0, 0], self.rotation_degrees, raylib.WHITE)

        super().editor_update(origin_offset)

    def game_update(self):
        super().game_update()

        if self.sprite_path:
            raylib.DrawTexturePro(self.image, [0.0, 0.0, self.image_width, self.image_height], [int(self.position.x - (self.image_width * self.scale.x) / 2), int(self.position.y - (self.image_height * self.scale.y) / 2), self.image_width * self.scale.x, self.image_height * self.scale.y], [0, 0], self.rotation_degrees, raylib.WHITE)

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
            "rotation": self.rotation,
            "sprite_path": self.sprite_path if self.sprite_path else "None"
        }
    
    def load_self(self, node):
        super().load_self(node)
    
        self.sprite_path = node["sprite_path"] if node["sprite_path"] != "None" else None
        if self.sprite_path:
            self.set_texture(self.sprite_path)


class Shape(Position):
    def __init__(self):
        Position.__init__(self)

        # Set node_type
        self.node_type = "Shape"

        # Shape type
        self.shape_index = global_enumerations.SHAPE_RECT

        # Rectangle values
        self.width = 50
        self.height = 50

        # Circle values
        self.radius = 50

        # Line/Polygon Values
        self.points = [(0, 0), (50, 50), (20, 40)]
        self.points_real_positions = [(0, 0), (50, 50), (20, 40)]
        
        # Polygon Values
        self.triangulated_polygon = self._triangulate_polygon(self.points)

        # All values (effects every type)
        self.color = (0, 0, 0, 255)

    def editor_update(self, origin_offset):
        offset_position = self.position + origin_offset

        if self.just_moved:
            for point_index in range(len(self.points)):
                self.points_real_positions[point_index] = (self.points[point_index][0] + offset_position.x, self.points[point_index][1] + offset_position.y)

            self.triangulated_polygon = self._triangulate_polygon(self.points_real_positions)

        if self.shape_index == global_enumerations.SHAPE_RECT:
            raylib.DrawRectangle(int(offset_position.x - self.width / 2), int(offset_position.y - self.height / 2), int(self.width), int(self.height), self.color)
        
            # Draw rectangle resize UI only if node is selected.
            if self.selected:
                raylib.DrawRectangleLines(int(offset_position.x - self.width / 2), int(offset_position.y - self.height / 2), int(self.width), int(self.height), raylib.YELLOW)

                # Get mouse position.
                mouse_position = raylib.GetMousePosition()

                # Draw resize circles for rectangle corners.
                raylib.DrawCircleLines(int(offset_position.x - self.width / 2), int(offset_position.y - self.height / 2), 5, raylib.YELLOW)
                raylib.DrawCircleLines(int(offset_position.x + self.width / 2), int(offset_position.y - self.height / 2), 5, raylib.YELLOW)
                raylib.DrawCircleLines(int(offset_position.x - self.width / 2), int(offset_position.y + self.height / 2), 5, raylib.YELLOW)
                raylib.DrawCircleLines(int(offset_position.x + self.width / 2), int(offset_position.y + self.height / 2), 5, raylib.YELLOW)

                # Initialize buttons for rectangle corners.
                top_left_corner_button     = InvisibleButton(offset_position.x - self.width / 2 - 10, offset_position.y - self.height / 2 - 10, 20, 20)
                top_right_corner_button    = InvisibleButton(offset_position.x + self.width / 2 - 10, offset_position.y - self.height / 2 - 10, 20, 20)
                bottom_left_corner_button  = InvisibleButton(offset_position.x - self.width / 2 - 10, offset_position.y + self.height / 2 - 10, 20, 20)
                bottom_right_corner_button = InvisibleButton(offset_position.x + self.width / 2 - 10, offset_position.y + self.height / 2 - 10, 20, 20)

                # Get outputs from buttons this frame.
                top_left_corner_button_output     = top_left_corner_button.update()
                top_right_corner_button_output    = top_right_corner_button.update()
                bottom_left_corner_button_output  = bottom_left_corner_button.update()
                bottom_right_corner_button_output = bottom_right_corner_button.update()

                # Math for handling movement of corners!
                if top_left_corner_button_output == global_enumerations.BUTTON_PRESSED:
                    corner_offset_x = offset_position.x - self.width / 2 - mouse_position.x
                    corner_offset_y = offset_position.y - self.height / 2 - mouse_position.y

                    self.add_position(pygame.Vector2(-corner_offset_x * (1/3), -corner_offset_y * (1/3)))
                    self.width += corner_offset_x * (2/3)
                    self.height += corner_offset_y * (2/3)

                if top_right_corner_button_output == global_enumerations.BUTTON_PRESSED:
                    corner_offset_x = mouse_position.x - (offset_position.x + self.width / 2)
                    corner_offset_y = offset_position.y - self.height / 2 - mouse_position.y

                    self.add_position(pygame.Vector2(corner_offset_x * (1/3), -corner_offset_y * (1/3)))
                    self.width += corner_offset_x * (2/3)
                    self.height += corner_offset_y * (2/3)

                if bottom_left_corner_button_output == global_enumerations.BUTTON_PRESSED:
                    corner_offset_x = offset_position.x - self.width / 2 - mouse_position.x
                    corner_offset_y = mouse_position.y - (offset_position.y + self.height / 2)

                    self.add_position(pygame.Vector2(-corner_offset_x * (1/3), corner_offset_y * (1/3)))
                    self.width += corner_offset_x * (2/3)
                    self.height += corner_offset_y * (2/3)

                if bottom_right_corner_button_output == global_enumerations.BUTTON_PRESSED:
                    corner_offset_x = mouse_position.x - (offset_position.x + self.width / 2)
                    corner_offset_y = mouse_position.y - (offset_position.y + self.height / 2)

                    self.add_position(pygame.Vector2(corner_offset_x * (1/3), corner_offset_y * (1/3)))
                    self.width += corner_offset_x * (2/3)
                    self.height += corner_offset_y * (2/3)

        if self.shape_index == global_enumerations.SHAPE_CIRCLE:
            raylib.DrawCircle(int(offset_position.x), int(offset_position.y), self.radius, self.color)

            if self.selected:
                # Get mouse position.
                mouse_position = raylib.GetMousePosition()

                # Draw yellow selection icons.
                raylib.DrawCircleLines(int(offset_position.x), int(offset_position.y), self.radius, raylib.YELLOW)
                raylib.DrawCircleLines(int(offset_position.x + self.radius), int(offset_position.y), 5, raylib.YELLOW)

                # Button for changing radius.
                change_radius_button = InvisibleButton(int(offset_position.x + self.radius - 10), int(offset_position.y - 10), 20, 20)
                change_radius_button_output = change_radius_button.update()

                # Change radius if mouse is dragging.
                if change_radius_button_output == global_enumerations.BUTTON_PRESSED:
                    self.radius = mouse_position.x - offset_position.x

        if self.shape_index == global_enumerations.SHAPE_LINE:
            raylib.DrawLineStrip(self.points_real_positions, len(self.points), self.color)

            if self.selected:
                # Get mouse position.
                mouse_position = raylib.GetMousePosition()

                for point in self.points_real_positions:
                    # Draw yellow selection icon on each point.
                    raylib.DrawCircleLines(int(point[0]), int(point[1]), 5, raylib.YELLOW)

                    # Button for moving point.
                    change_point_button = InvisibleButton(int(point[0] - 10), int(point[1] - 10), 20, 20)
                    change_point_button_output = change_point_button.update()

                    # Change point if mouse is dragging.
                    if change_point_button_output == global_enumerations.BUTTON_PRESSED:
                        self.points[self.points_real_positions.index(point)] = (mouse_position.x - offset_position.x, mouse_position.y - offset_position.y)
                       
                        for point_index in range(len(self.points)):
                            self.points_real_positions[point_index] = (self.points[point_index][0] + offset_position.x, self.points[point_index][1] + offset_position.y)

        if self.shape_index == global_enumerations.SHAPE_POLYGON:
            for triangle in self.triangulated_polygon:
                raylib.DrawTriangle(triangle[0], triangle[1], triangle[2], self.color)

            if self.selected:
                # Get mouse position.
                mouse_position = raylib.GetMousePosition()

                for point in self.points_real_positions:
                    # Draw yellow selection icon on each point.
                    raylib.DrawCircleLines(int(point[0]), int(point[1]), 5, raylib.YELLOW)

                    # Button for moving point.
                    change_point_button = InvisibleButton(int(point[0] - 10), int(point[1] - 10), 20, 20)
                    change_point_button_output = change_point_button.update()

                    # Change point if mouse is dragging.
                    if change_point_button_output == global_enumerations.BUTTON_PRESSED:
                        self.points[self.points_real_positions.index(point)] = (mouse_position.x - offset_position.x, mouse_position.y - offset_position.y)
                       
                        for point_index in range(len(self.points)):
                            self.points_real_positions[point_index] = (self.points[point_index][0] + offset_position.x, self.points[point_index][1] + offset_position.y)

                        self.triangulated_polygon = self._triangulate_polygon(self.points_real_positions)

        super().editor_update(origin_offset)

    def game_update(self):
        super().game_update()

        if self.shape_index == global_enumerations.SHAPE_RECT:
            raylib.DrawRectangle(int(self.position.x - self.width / 2), int(self.position.y - self.height / 2), int(self.width), int(self.height), self.color)
        
        if self.shape_index == global_enumerations.SHAPE_CIRCLE:
            raylib.DrawCircle(int(self.position.x), int(self.position.y), self.radius, self.color)

        if self.shape_index == global_enumerations.SHAPE_LINE:
            raylib.DrawLineStrip(self.points, len(self.points), self.color)

        if self.shape_index == global_enumerations.SHAPE_POLYGON:
            for triangle in self.triangulated_polygon:
                raylib.DrawTriangle(triangle[0], triangle[1], triangle[2], self.color)

    def _triangulate_polygon(self, points):
        unsorted_triangles = tripy.earclip(points)

        # Sort triangles counterclockwise.
        for triangle in range(len(unsorted_triangles)):
            numpy_array = numpy.array([unsorted_triangles[triangle][0], unsorted_triangles[triangle][1], unsorted_triangles[triangle][2]])
            center_x, center_y = numpy_array.mean(0)
            x, y = numpy_array.T
            angles = numpy.arctan2(x - center_x, y - center_y)
            indices = numpy.argsort(angles)
            regular_array = numpy_array[indices].tolist()
            unsorted_triangles[triangle] = regular_array

        return unsorted_triangles

    def update_polygon_points(self, points):
        self.points_real_positions = points
        self.triangulated_polygon = self._triangulate_polygon(points)

    def get_properties_dict(self):
        # Convert points list to json acceptable format.
        converted_points = []

        for point in self.points:
            converted_points.append(list(point))

        return {
            "type": "Shape", 
            "name": self.name,
            "script_path": self.script_path, 
            "children": [self.children[i].get_properties_dict() for i in range(len(self.children))], 
            "position_x": self.position.x,
            "position_y": self.position.y, 
            "scale_x": self.scale.x,
            "scale_y": self.scale.y,
            "rotation": self.rotation,
            "shape_index": self.shape_index,
            "rectangle_width": self.width,
            "rectangle_height": self.height,
            "circle_radius": self.radius,
            "points": converted_points,
        }

    def load_self(self, node):
        super().load_self(node)
    
        self.shape_index = node["shape_index"]
        self.width = node["rectangle_width"]
        self.height = node["rectangle_height"]
        self.radius = node["circle_radius"]
        self.points = node["points"]
        self.triangulated_polygon = self._triangulate_polygon(self.points)