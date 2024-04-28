import raylib
import resources.timer
import os
from resources import global_enumerations


if os.path.exists("assets/Arimo-VariableFont_wght.ttf"):
    FONT = raylib.LoadFont(b"assets/Arimo-VariableFont_wght.ttf")
else:
    FONT = raylib.LoadFont(os.path.join(os.path.dirname(__file__), "Arimo-VariableFont_wght.ttf").encode("utf-8"))


class Button:
    def __init__(self, x, y, width, height, border_width, border_radius, border_color, fill_color, text, text_color, font_path, font_size):
        self.x, self.y, self.width, self.height, self.border_width, self.border_radius, self.border_color, self.fill_color, self.font_size, self.text, self.text_color = x, y, width, height, border_width, border_radius, border_color, fill_color, font_size, text if not isinstance(text, str) else text.encode("ascii"), text_color
        self.held_down_timer = resources.timer.Timer(0.5, False, True)
        self.held_down = False

    def update(self):
        raylib.DrawRectangleRounded((self.x, self.y, self.width, self.height), self.border_radius, 1, self.fill_color)
        raylib.DrawRectangleRoundedLines((self.x, self.y, self.width, self.height), self.border_radius, 1, self.border_width, self.border_color)

        text_size = raylib.MeasureTextEx(FONT, self.text, self.font_size, 3)
        raylib.DrawTextEx(FONT, self.text, (self.x + self.width / 2 - text_size.x / 2, self.y + self.height / 2 - text_size.y / 2), self.font_size, 3, self.text_color)

        mouse_pos = raylib.GetMousePosition()

        if mouse_pos.x > self.x and mouse_pos.x < self.x + self.width and mouse_pos.y > self.y and mouse_pos.y < self.y + self.height:
            mouse_just_pressed = raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT)
            mouse_pressed = raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT)
            
            if mouse_just_pressed:
                return global_enumerations.BUTTON_JUST_PRESSED
            
            if mouse_pressed:
                return global_enumerations.BUTTON_PRESSED

            if mouse_pressed:
                self.held_down_timer.start()
            else:
                self.held_down_timer.stop()
                self.held_down = False
        else:
            self.held_down_timer.stop()
            self.held_down = False

        increase_fast = self.held_down_timer.update(raylib.GetFrameTime())

        if increase_fast:
            self.held_down = True

        if self.held_down:
            return global_enumerations.BUTTON_NOT_INTERACTED

        return global_enumerations.BUTTON_NOT_INTERACTED
    
class InvisibleButton:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.held_down_timer = resources.timer.Timer(0.5, False, True)
        self.held_down = False

    def update(self):
        mouse_pos = raylib.GetMousePosition()

        if mouse_pos.x > self.x and mouse_pos.x < self.x + self.width and mouse_pos.y > self.y and mouse_pos.y < self.y + self.height:
            mouse_just_pressed = raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT)
            mouse_pressed = raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT)
            
            if mouse_just_pressed:
                return global_enumerations.BUTTON_JUST_PRESSED
            
            if mouse_pressed:
                return global_enumerations.BUTTON_PRESSED

            if mouse_pressed:
                self.held_down_timer.start()
            else:
                self.held_down_timer.stop()
                self.held_down = False

            return global_enumerations.BUTTON_HOVERED
        else:
            self.held_down_timer.stop()
            self.held_down = False

        increase_fast = self.held_down_timer.update(raylib.GetFrameTime())

        if increase_fast:
            self.held_down = True

        if self.held_down:
            return global_enumerations.BUTTON_NOT_INTERACTED

        return global_enumerations.BUTTON_NOT_INTERACTED