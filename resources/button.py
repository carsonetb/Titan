import pygame
import pygame.gfxdraw
import raylib


FONT = raylib.LoadFont(b"assets/Arimo-VariableFont_wght.ttf")


class Button:
    def __init__(self, x, y, width, height, border_width, border_radius, border_color, fill_color, text, text_color, font_path, font_size):
        self.x, self.y, self.width, self.height, self.border_width, self.border_radius, self.border_color, self.fill_color, self.font_size, self.text, self.text_color = x, y, width, height, border_width, border_radius, border_color, fill_color, font_size, text, text_color

    def update(self):
        raylib.DrawRectangleRounded((self.x, self.y, self.width, self.height), self.border_radius, 1, self.fill_color)
        raylib.DrawRectangleRoundedLines((self.x, self.y, self.width, self.height), self.border_radius, 1, self.border_width, self.border_color)

        #window.blit(self.text_surf, (self.x + self.width / 2 - self.text_surf.get_width() / 2, self.y + self.height / 2 - self.text_surf.get_height() / 2))
        text_size = raylib.MeasureTextEx(FONT, self.text, self.font_size, 3)
        raylib.DrawTextEx(FONT, self.text, (self.x + self.width / 2 - text_size.x / 2, self.y + self.height / 2 - text_size.y / 2), self.font_size, 3, self.text_color)

        mouse_pos = raylib.GetMousePosition()

        if mouse_pos.x > self.x and mouse_pos.x < self.x + self.width and mouse_pos.y > self.y and mouse_pos.y < self.y + self.height:
            mouse_pressed = raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT)
            if mouse_pressed:
                return 1

        return 0