import raylib


class Hierarchy:
    """Hierarchy for NODES"""

    def __init__(self, x, y, width):
        self.items = []
        self.selected_item = None
        self.x, self.y, self.width = x, y, width
        self.item_font = raylib.LoadFont(b"assets/Arimo-VariableFont-wght.ttf")

    def recurse_draw_list(self, to_draw, index, depth):
        for i in range(len(to_draw)):
            try:
                to_draw[i].name
                
                index += 1
                draw_depth = depth

                if i == 0:
                    draw_depth = depth - 1

                mouse_pos = raylib.GetMousePosition()

                if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                    if mouse_pos.x > self.x and mouse_pos.x < self.x + self.width and mouse_pos.y > self.y + index * 25 - 10 and mouse_pos.y < self.y + index * 25 - 3 + 27:
                        self.selected_item = to_draw[i]

                if to_draw[i] == self.selected_item:
                    to_draw[i].selected = True
                    raylib.DrawRectangle(self.x - 20, self.y + index * 25 - 3, self.width + 20, 27, (150, 150, 150, 255))
                else:
                    to_draw[i].selected = False
                
                raylib.DrawTextEx(self.item_font, bytes(to_draw[i].name, 'utf-8'), (self.x + 10 + draw_depth * 20, self.y + index * 25), 20, 2, (0, 0, 0, 255))

            except:
                index = self.recurse_draw_list(to_draw[i], index, depth + 1)
        
        return index

class List:
    """Non-hierarchy for STRINGS"""

    def __init__(self, x, y, width):
        self.items = []
        self.selected_item = None
        self.x, self.y, self.width = x, y, width
        self.item_font = raylib.LoadFont(b"assets/Arimo-VariableFont-wght.ttf")
    
    def draw_list(self, to_draw):
        index = 0
        
        for i in range(len(to_draw)):
            index += 1

            mouse_pos = raylib.GetMousePosition()

            if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                if mouse_pos.x > self.x and mouse_pos.x < self.x + self.width and mouse_pos.y > self.y + index * 25 - 10 and mouse_pos.y < self.y + index * 25 - 3 + 27:
                    self.selected_item = to_draw[i]

            if to_draw[i] == self.selected_item:
                raylib.DrawRectangle(int(self.x - 20), int(self.y + index * 25 - 3), int(self.width + 20), 27, (150, 150, 150, 255))
            
            raylib.DrawTextEx(self.item_font, bytes(to_draw[i], 'utf-8'), (self.x + 10, self.y + index * 25), 20, 2, (0, 0, 0, 255))