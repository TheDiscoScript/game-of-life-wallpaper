import logging
import subprocess
import time
import os
import random
from PIL import Image, ImageDraw
from dotenv import load_dotenv


load_dotenv()

# Configure logging
logging_path=os.getenv("BASE_LOGGING_PATH")
logging.basicConfig(filename=logging_path, level=logging.DEBUG, format='%(asctime)s %(message)s')

def set_wallpaper(image_path):
    try:
        #AppleScript force the wallpaper change
        applescript = f'''
        tell application "System Events"
            set desktopCount to count of desktops
            repeat with desktopNumber from 1 to desktopCount
                tell desktop desktopNumber
                    set picture to "{image_path}"
                end tell
            end repeat
        end tell
        '''
        subprocess.run(['osascript', '-e', applescript], check=True) # execute the command
        logging.debug("Wallpaper set successfully using AppleScript")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set wallpaper using AppleScript: {e}")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")

def create_game_of_life_image(base_path, iteration, grid, cell_size):
    try:
        image_path = f"{base_path}_{iteration}.png"
        width, height = len(grid[0]) * cell_size, len(grid) * cell_size
        image = Image.new('RGB', (width, height), (0, 0, 0)) #BG color
        draw = ImageDraw.Draw(image)

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x]:
                    draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size - 1, (y + 1) * cell_size - 1], fill=(255, 105, 180)) #PINK alive

        image.save(image_path)
        logging.debug(f"Image saved at {image_path} with iteration {iteration}")
        return image_path
    except Exception as e:
        logging.error(f"Exception occurred while creating image: {e}")
        return None

def update_grid(grid):
    new_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            live_neighbors = sum([grid[(y + dy) % len(grid)][(x + dx) % len(grid[0])] for dy in range(-1, 2) for dx in range(-1, 2)]) - grid[y][x]
            if grid[y][x] == 1 and live_neighbors in [2, 3]:
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and live_neighbors == 3:
                new_grid[y][x] = 1
    return new_grid

def create_initial_grid(cols, rows):
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

base_wallpaper_path = os.getenv("BASE_WALLPAPER_PATH")
iteration = 0 #0
cell_size = 15 #10 # size of each cell in pixels - performance impact
cols, rows = 100, 80  # grid size #80, 60

# Init Game of Life grid
grid = create_initial_grid(cols, rows)

while True:
    image_path = create_game_of_life_image(base_wallpaper_path, iteration, grid, cell_size)
    if image_path:
        set_wallpaper(image_path)
        logging.debug(f'Wallpaper updated for iteration {iteration}')
        iteration += 1
        grid = update_grid(grid)
        time.sleep(0.5)  # seconds interval for render update

    # Cleanup old images
    if iteration > 1:
        try:
            os.remove(f"{base_wallpaper_path}_{iteration-2}.png")
        except FileNotFoundError:
            pass
