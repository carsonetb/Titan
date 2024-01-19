import pygame
import pygame.gfxdraw


class Button:
    def __init__(self, x, y, width, height, border_width, border_radius, border_color, fill_color, text, text_color, font, font_size):
        self.x, self.y, self.width, self.height, self.border_width, self.border_radius, self.border_color, self.fill_color = x, y, width, height, border_width, border_radius, border_color, fill_color
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surf = self.font.render(text, True, text_color)

    def update(self, window):
        pygame.draw.rect(window, self.fill_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
        pygame.draw.rect(window, self.border_color, (self.x, self.y, self.width, self.height), self.border_width, self.border_radius)

        window.blit(self.text_surf, (self.x + self.width / 2 - self.text_surf.get_width() / 2, self.y + self.height / 2 - self.text_surf.get_height() / 2))

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed:
                return 1

        return 0