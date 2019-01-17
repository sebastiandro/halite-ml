import os
import secrets

MAX_TURNS = 50

map_settings = {32: 400, 40: 425, 48: 450, 56: 475, 64: 500}


while True:
    map_size = secrets.choice(list(map_settings.keys()))
    commands = [
        f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --width {map_size} --height {map_size} "python3 valter-vit.py" "python3 valter-vit.py"',
        f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --width {map_size} --height {map_size} "python3 valter-vit.py" "python3 valter-vit.py"']

    command = secrets.choice(commands)
    os.system(command)
