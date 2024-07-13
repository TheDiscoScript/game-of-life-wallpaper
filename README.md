# Dynamic Game of Life Wallpaper

This project creates a dynamic wallpaper for macOS using Conway's Game of Life. The wallpaper updates at regular intervals to reflect the current state of the simulation.

## Installation of Dependencies

To run this project, you need to have Python installed. Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

Create a .env file in the root directory and add your configuration:

```
BASE_WALLPAPER_PATH=/path/to/your/wallpaper
BASE_LOGGING_PATH=/tmp/wallpaper_test.log
```

## How to Run

Run the script using the following command:

```
python game-of-life.py
```

You can also set up a LaunchAgent to run the script in the background:
Create a plist file in ~/Library/LaunchAgents/ (e.g., com.yourname.gameoflifewallpaper.plist).
Add the following content, replacing the paths with your script's path:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourname.gameoflifewallpaper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/game-of-life.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load the LaunchAgent:

```
launchctl load ~/Library/LaunchAgents/com.yourname.gameoflifewallpaper.plist
```

To unload the LaunchAgent:

```
launchctl unload ~/Library/LaunchAgents/com.yourname.gameoflifewallpaper.plist
```

### Customization

You can customize the following parameters in the script:

cell_size: The size of each cell in the Game of Life grid.

cols and rows: The number of columns and rows in the grid.

time.sleep(5): The interval between wallpaper updates.
