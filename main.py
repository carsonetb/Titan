import raylib
import multiprocessing
import sys
import os

import editor_main






#
#  __  __                       _        _                             _ _    ______ _____  ______ _____  
# |  \/  |                     | |      (_)                           | | |  |  ____|  __ \|  ____|  __ \ 
# | \  / |_   _    ___ ___   __| | ___   _ ___    __ _  ___   ___   __| | |  | |__  | |__) | |__  | |__) |
# | |\/| | | | |  / __/ _ \ / _` |/ _ \ | / __|  / _` |/ _ \ / _ \ / _` | |  |  __| |  _  /|  __| |  _  / 
# | |  | | |_| | | (_| (_) | (_| |  __/ | \__ \ | (_| | (_) | (_) | (_| |_|  | |    | | \ \| |    | | \ \ 
# |_|  |_|\__, |  \___\___/ \__,_|\___| |_|___/  \__, |\___/ \___/ \__,_(_)  |_|    |_|  \_\_|    |_|  \_\
#          __/ |                                  __/ |                                                   
#         |___/                                  |___/     








def main_process(local_data_path):
    # Initialize Main Menu
    main_menu = editor_main.TitanMainMenu(local_data_path)

    while not raylib.WindowShouldClose():
        main_menu.update()
    
    main_menu.prepare_for_close()
    raylib.CloseWindow()

if __name__ == "__main__":
    # On Windows calling this function is necessary.
    multiprocessing.freeze_support()

    # Check if the projects.json file exists in the appdata | .local/share directories.
    print("INFO: Initialising engine skeleton. Checking/preparing files to start engine.")

    if sys.platform.startswith("win"):
        print("INFO: Detected platform Windows.")
        appdata_path = os.getenv("LOCALAPPDATA")

    elif sys.platform.startswith("linux"):
        print("INFO: Detected platform Linux.")

        # This might not work on Linux. Currently untested.
        appdata_path = f"{os.getenv('HOME')}/.local/share"

    elif sys.platform.startswith("darwin"):
        print("INFO: Detected platform MacOS.")

        # This might not work on MacOS. Currently untested.
        appdata_path = f"{os.getenv('HOME')}/.local/share"

    else:
        print(f"WARNING: Detected unfamiliar platform: '{sys.platform}'. Assuming Linux-like distribution.")

        # This might not work on Linux. Currently untested.
        appdata_path = "~/.local/share"
    
    titan_folder_exists = os.path.exists(appdata_path + "/TitanLocal")

    if titan_folder_exists:
        print("INFO: Detected already existant Titan local data folder.")

        projects_file_exists = os.path.exists(appdata_path + "/TitanLocal/projects.json")

        if projects_file_exists:
            print("INFO: Projects file already existant. Ready to start.")
        else:
            print("INFO: Projects file doesn't exist. Creating ...")

            projects_file = open(appdata_path + "/TitanLocal/projects.json", "x")
            projects_file.write("[]")
            projects_file.close()
    else:
        print("INFO: Titan local data folder is nonexistant. Creating ...")

        os.mkdir(appdata_path + "/TitanLocal")

        projects_file = open(appdata_path + "/TitanLocal/projects.json", "x")
        projects_file.write("[]")
        projects_file.close()
    
    print("INFO: Engine skeleton ready. Starting main process.")
    main_process(appdata_path + "/TitanLocal")
