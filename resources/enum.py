import raylib
import pygame
import resources.button
import resources.list

class EnumStorage:
    def __init__(self, enum: dict, start_item: str):
        self.enum = enum
        self.item_selected = start_item

class EnumSelectionMenu:
    def __init__(self, enum: dict, start_item: str, x, y, width, height, border_radius, font_size):
        self.enum = EnumStorage(enum, start_item)
        self.selection_button = None
        self.selection_menu = resources.list.List(x, y + height, width)
        self.menu_visible = False

        self.position = pygame.Vector2(x, y)
        self.dimensions = pygame.Vector2(width, height)
        self.border_radius = border_radius
        self.font_size = font_size

        self.reload_button()

    def update(self):
        selected = self.selection_button.update()
        self.selection_menu.x = self.position.x
        self.selection_button.x = self.position.x

        if self.menu_visible:
            self.selection_menu.draw_list(list(self.enum.enum.keys()))

            if self.selection_menu.selected_item:
                self.enum.item_selected = self.selection_menu.selected_item
                self.menu_visible = False
                self.selection_menu.selected_item = None
                self.reload_button()
                
                return 1
        
        if selected:
            self.menu_visible = True
        elif raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            self.menu_visible = False
        
        return 0

    def reload_button(self):
        self.selection_button = resources.button.Button(self.position.x, self.position.y, self.dimensions.x, self.dimensions.y, 1, self.border_radius, raylib.BLACK, raylib.WHITE, self.enum.item_selected, raylib.BLACK, "loller", self.font_size)