import pygame
import importlib
import sys
from node_types.position import Position
from node_types.sprite import Sprite
from pygame import gfxdraw

pygame.init()
pygame.font.init()

REG_FONT = pygame.font.SysFont("arial", 32)


class EditorHandler:
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.top_level_nodes = []
        self.background_color = pygame.Vector3(255, 255, 255)
        self.left_sidebar_width = 300
        self.origin_offset = pygame.Vector2(self.left_sidebar_width, 0)

    def update(self):
        self.window.fill(self.background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

        for node in self.top_level_nodes:
            node.editor_update(self.window, self.origin_offset)

        pygame.draw.rect(self.window, (200, 200, 200), (0, 0, self.left_sidebar_width, self.window.get_height()))
        gfxdraw.line(self.window, self.left_sidebar_width, 0, self.left_sidebar_width, self.window.get_height(), (0, 0, 0))

        nodes = []

        for node in self.top_level_nodes:
            nodes += node.get_children_recursive()

        for i in range(len(nodes)):
            node_text = REG_FONT.render(nodes[i].name, True, (0, 0, 0))
            self.window.blit(node_text, (10, 10 + i * 30))

        pygame.display.update()


def main():
    # Initialize Editor
    editor = EditorHandler(1800, 1000)

    # Load sprite node to add to scene.
    sprite = Sprite("/home/cbates8923/TitanEngine/assets/logo.png")
    sprite.load_script("/home/cbates8923/TitanEngine/test_scripts/test_script.py")

    # Add to nodes.
    editor.top_level_nodes.append(sprite)

    while True:
        action_code = editor.update()

        if action_code == 1:
            break
    

if __name__ == "__main__":
    main()