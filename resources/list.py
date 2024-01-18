import pygame


class Hierarchy:
    def __init__(self, x, y, width):
        self.items = []
        self.selected_item = None
        self.x, self.y, self.width = x, y, width
        self.item_font = pygame.font.SysFont("arial", 20)

    def recurse_draw_list(self, window, to_draw, index, depth):
        for i in range(len(to_draw)):
            try:
                to_draw[i].name
                index += 1
                draw_depth = depth

                if i == 0:
                    draw_depth = depth - 1

                mouse_pos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y + index * 25 - 10 and mouse_pos[1] < self.y + index * 25 - 3 + 27:
                        self.selected_item = to_draw[i]

                if to_draw[i] == self.selected_item:
                    to_draw[i].selected = True
                    pygame.draw.rect(window, (150, 150, 150), (self.x - 20, self.y + index * 25 - 3, self.width + 20, 27))
                else:
                    to_draw[i].selected = False
                
                node_name_text = self.item_font.render(to_draw[i].name, True, (0, 0, 0))
                window.blit(node_name_text, (self.x + 10 + draw_depth * 20, self.y + index * 25))

            except:
                index = self.recurse_draw_list(window, to_draw[i], index, depth + 1)
        
        return index
