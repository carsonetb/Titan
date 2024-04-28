import raylib

import editor_main

def main_process():
    # Initialize Main Menu
    main_menu = editor_main.TitanMainMenu()

    while not raylib.WindowShouldClose():
        main_menu.update()
    
    main_menu.prepare_for_close()
    raylib.CloseWindow()

if __name__ == "__main__":
    main_process()