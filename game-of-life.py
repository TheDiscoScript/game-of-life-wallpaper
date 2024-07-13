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
logging.basicConfig(filename=logging_path, level=logging.ERROR, format='%(asctime)s %(message)s')

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

        # y = row index, row = row values
        for y, row in enumerate(grid):
            # x = col index, cell = cell value 0 or 1
            for x, cell in enumerate(row):
                if cell:
                    #calculate corners of alive cell
                    top_left = (x * cell_size, y * cell_size)
                    bottom_right = ((x + 1) * cell_size - 1, (y + 1) * cell_size - 1)
                    draw.rectangle([top_left, bottom_right], fill=(255, 105, 180)) # Pink color = Alive cell

        image.save(image_path)
        logging.debug(f"Image saved at {image_path} with iteration {iteration}")
        return image_path
    except Exception as e:
        logging.error(f"Exception occurred while creating image: {e}")
        return None

def update_grid(grid):
    # 8 positions agains center cell
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # new grid with same proportions with dead cells
    new_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            # Count live neighbors - sums values of 8 positions around the cell
            live_neighbors = sum(
                grid[(y + dy) % len(grid)][(x + dx) % len(grid[0])]
                for dy, dx in directions
            )

            # Apply the Game of Life rules
            if cell == 1:  # Current cell is alive
                if live_neighbors in [2, 3]:
                    new_grid[y][x] = 1  # Stays alive
            else:  # Current cell is dead
                if live_neighbors == 3:
                    new_grid[y][x] = 1  # Becomes alive
    return new_grid

def create_initial_grid(cols, rows):
    # Initialize the grid with random live (1) and dead (0) cells
    grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
    return grid

base_wallpaper_path = os.getenv("BASE_WALLPAPER_PATH")
iteration = 0 #0
cell_size = 12 #10 # size of each cell in pixels - performance impact
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
