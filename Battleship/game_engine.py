# Game Engine
import random

class Ship:
    def __init__(self, size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["h","v"])
        self.indexes = self.compute_indexes()
    
    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i*10 for i in range(self.size)]
        
class Player():
    def __init__(self):
        self.ships = []
        self.search = ["U"  for i in range(100)] # "U" for "Unknown"
        self.place_ships(sizes = [5, 4, 3, 3, 2])
        list_of_list = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_list for index in sublist]

    def place_ships(self,sizes):
        for size in sizes:
            placed = False
            while not placed:

                # Create a new ship
                ship = Ship(size)

                # check if placement is possible
                placement_possible = True
                for i in ship.indexes:

                    # indexes must be < 100
                    if i >= 100:
                        placement_possible = False
                        break
                    # board edges are not connected
                    new_row = i//10
                    new_col = i%10
                    if new_row != ship.row and new_col !=ship.col:
                        placement_possible = False
                        break
                    # ship cannot intersect
                    for placed_ship in self.ships:
                        if i in placed_ship.indexes:
                            placement_possible = False
                            break
                    
                    # if possible, place that ship

                if placement_possible:
                    self.ships.append(ship)
                    placed = True

    def show_ships(self):
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)]
        for row in range(10):
            print(" ".join(indexes[(row-1)*10:row*10]))


class AIPlayer(Player):
    # needs to change the player1 board

    def AI_move(self, mode = None):
        if (mode == "diagonal_skewer"):
           None
        elif (mode == None):
            moves = set(range(100))
            selected_move = random.choice(list(moves))
            moves.remove(selected_move)
        return int(selected_move)

    def heuristic(self):
        None
    def choose_possible_move(self):
        None

class BattleShipGame():

    def __init__(self):
        self.player1 = Player()
        self.player2 = AIPlayer()
        self.player1_turn = 1
        self.over = 0

    def change_turn(self):
        if self.player1_turn == 1:
            self.player1_turn = 0
        else:
            self.player1_turn = 1

    def make_move(self, i):

        active_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1

        # set miss "M" or hit "H"
        if i in opponent.indexes:
            active_player.search[i] = "H"
            # check if ship is sunk ("S")
            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if active_player.search[i] == "U":
                        sunk = False
                        break
                if sunk:
                    for i in ship.indexes:
                        active_player.search[i] = "S"
                        
        else:
            active_player.search[i] = "M"
            self.change_turn()

        # change the active player



