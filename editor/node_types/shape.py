import pygame
import raylib
import tripy
import numpy

import resources.misc
from resources import global_enumerations
from resources.button import InvisibleButton
from node_types.position import Position
from scripting.shape_engine_interactable import ShapeEngineInteractable

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
        offset_position = self.global_position + origin_offset

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
            raylib.DrawRectanglePro([int(self.global_position.x), int(self.global_position.y), int(self.width), int(self.height)], [self.width / 2, self.height / 2], resources.misc.rad_to_deg(self.rotation), self.color)
        
        if self.shape_index == global_enumerations.SHAPE_CIRCLE:
            raylib.DrawCircle(int(self.global_position.x), int(self.global_position.y), self.radius, self.color)

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

    def update_variables_from_interactable(self, engine_interactable: ShapeEngineInteractable):
        super().update_variables_from_interactable(engine_interactable)

        self.shape_index = engine_interactable.shape_type
        self.width = engine_interactable.rect_dimensions.x
        self.height = engine_interactable.rect_dimensions.y
        self.radius = engine_interactable.circle_radius
        self.points = engine_interactable.points
        self.color = engine_interactable.color

    def generate_engine_interactable(self):
        return ShapeEngineInteractable(
            self.children, 
            self.parent, 
            self.position,
            self.global_position, 
            self.rotation, 
            self.scale,
            self.shape_index,
            self.width,
            self.height,
            self.radius,
            self.points,
            self.color,
        )

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
