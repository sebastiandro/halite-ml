#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import secrets
import logging
import numpy as np
import time

game = hlt.Game()

constants.MAX_TURNS

TOTAL_TURNS = 50
SAVE_THRESHOLD = 4100
MAX_SHIPS = 1
SIGHT_DISTANCE = 16

direction_order = [Direction.North, Direction.East,
                   Direction.South, Direction.West, Direction.Still]

# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("ValterVit")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

training_data = []

ship_states = {}
while True:
    game.update_frame()

    me = game.me
    game_map = game.game_map
    command_queue = []

    dropoff_positions = [d.position for d in list(
        me.get_dropoffs()) + [me.shipyard]]
    ship_positions = [s.position for s in list(me.get_ships())]

    for ship in me.get_ships():

        size = SIGHT_DISTANCE
        surroundings = []
        for y in range(-1*size, size+1):
            row = []
            for x in range(-1*size, size+1):
                current_cell = game_map[ship.position + Position(x, y)]

                # Is this our ship or enemy ship?
                if current_cell.position in dropoff_positions:
                    drop_friend_foe = 1
                else:
                    drop_friend_foe = -1

                # Is this our ship or enemy ship?
                if current_cell.position in ship_positions:
                    ship_friend_foe = 1
                else:
                    ship_friend_foe = -1

                halite = round(current_cell.halite_amount /
                               constants.MAX_HALITE, 2)
                a_ship = current_cell.ship
                structure = current_cell.structure

                if halite is None:
                    halite = 0

                if a_ship is None:
                    a_ship = 0
                else:
                    a_ship = ship_friend_foe * \
                        round(a_ship.halite_amount / constants.MAX_HALITE, 2)

                if structure is None:
                    structure = 0
                else:
                    structure = drop_friend_foe

                amounts = (halite, a_ship, structure)

                row.append(amounts)

            surroundings.append(row)

        #np.save(f"game_play/{game.turn_number}.npy", surroundings)

        choice = secrets.choice(range(len(direction_order)))
        training_data.append([surroundings, choice])

        command_queue.append(ship.move(direction_order[choice]))

    if len(me.get_ships()) < MAX_SHIPS:
        if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
            command_queue.append(me.shipyard.spawn())

    if game.turn_number == TOTAL_TURNS:
        if me.halite_amount >= SAVE_THRESHOLD:
            np.save(
                f"training_data/{me.halite_amount}-{int(time.time()*1000)}.npy", training_data)
    game.end_turn(command_queue)
