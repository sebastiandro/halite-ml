#!/bin/sh

./halite --replay-directory replays/ --turn-limit 50 -vvv --width 32 --height 32 "python3 valter-vit.py" "python3 valter-vit-2.py"
