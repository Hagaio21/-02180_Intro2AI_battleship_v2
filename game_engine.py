# Game Engine
import random

START_PROBABILITY =         [8,11,14,15,16,16,15,14,11,8,
                            11,14,16,17,18,18,17,16,14,11,
                            14,16,18,19,19,19,19,18,16,14,
                            15,17,19,20,20,20,20,19,17,15,
                            16,18,19,20,21,21,20,19,18,16,
                            16,18,19,20,21,21,20,19,18,16,
                            15,17,19,20,20,20,20,19,17,15,
                            14,16,18,19,19,19,19,18,16,14,
                            11,14,16,17,18,18,17,16,14,11,
                            8,11,14,15,16,16,15,14,11,8]
def set_probability(player):
    update_indexes = []
    if not hasattr(player, "probability"):
        player.probability = START_PROBABILITY
    else:
        for index ,value in enumerate(player.search):
            if value == "M" or value == "H" or value == "S":
                update_indexes.append(index)
    for index in update_indexes:
        player.probability[index] = 0
    ############################################
    print(f"need to update {update_indexes} to 0")
    ############################################

            
def heuristic(player, move):
    p = player
    m = move
    if hasattr(p, 'mask'):
        h = p.probability[m]+p.mask[m]
    else:
        return 0
    return h

def best_move(player):
    best_m = player.moves[0]
    best_h = 0
    for m in player.moves:
        h = heuristic(player, m)
        if  h >= best_h:
            best_m = m
            best_h = h
    return m


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
    def __init__(self,name):
        self.name = name
        self.ships = []
        self.search = ["U"  for i in range(100)] # "U" for "Unknown"
        self.place_ships(sizes = [5, 4, 3, 3, 2])
        list_of_list = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_list for index in sublist]
        self.moves = list(set(range(100)))

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
    # def __init__(self):
    #     self.opponent_ships = [5,4,3,3,2]
    #     self.probability = [10]

    def AI_init(self, mode):
            # Innitiate AI player attibutes
            self.probability = START_PROBABILITY
            self.mask = [0 for i in range(100)]
            self.mode = mode
            self.turn = 0
            self.log = []

    # function that log states of AI.
    def AI_log_state(self):
        self.log.append({'probabilty': self.probability, 'mask': self.mask, 'moves': self.moves})


    def save_AI_log(self):
        text = ""
        for turn, l in enumerate(self.log):
            ms = l['mask']
            p = l['probabilty']
            m = l['moves']
            temp = f" turn{turn} \n mask: \n {ms} \n probability: \n {p} \n moves left: \n {m} "
            text = text + temp + "\n\n"
        filename = "Game_Log.txt"
        with open(filename, 'w') as file:
            file.write(text)
        print(f"File '{filename}' has been saved successfully.")


    def AI_move(self):
        if self.mode == "D": # if using diagonal skewer
    
            skewer = [num for num in list(self.moves) 
                      if (num // 10 % 2 == 0 and num % 2 == 0)
                        or (num // 10 % 2 != 0 and num % 2 != 0)]                                                                    
            if skewer:
                selected_move = random.choice(skewer)
            else:
                selected_move = random.choice(self.moves)

        elif self.mode == "R": # if using random mode

            selected_move = random.choice(self.moves)
            print(f"selected move is {selected_move}")

        elif self.mode == "H1": # if using heuristic

            selected_move = best_move(self)

        self.moves.remove(selected_move) # remove selected move from possible move list
        self.turn = self.turn + 1 # update turn counter
        self.AI_log_state()
        self.last_move = selected_move
        return int(selected_move)

           

    #mask works but only assigns ones
    
    def create_mask(self, i):
        row_index = i // 10
        col_index = i % 10
        # Set the values for the row
        for j in range(row_index * 10, (row_index + 1) * 10):
            if ((i-j) == 0):
                distance = 0
            else: 
                distance = round(1/(abs(i-j)*10),2)
            self.mask[j] = 1100*distance
        # Set the values for the column
        for j in range(col_index, 100, 10):
            if ((i-j) == 0):
                distance = 0
            else:
                distance = round(1/abs(i-j),2)
            self.mask[j] = 1100*distance
        

    # def create_mask(self, i):
    #     row_index = i // 10
    #     col_index = i % 10
        
    #     # Set the values for the cross
    #     for row in range(10):
    #         for col in range(10):
    #             distance = abs(row - row_index) + abs(col - col_index)
    #             self.mask[row * 10 + col] += max(0, 30 - distance * 5)
        
    #   

class BattleShipGame():

    def __init__(self):
        self.player1 = Player("Player1")
        self.player2 = AIPlayer("AI")
        self.player2.AI_init(mode='D')
        self.player1_turn = 1
        self.over = 0
        self.winner = None

    def change_turn(self):
        if self.player1_turn == 1:
            self.player1_turn = 0
        else:
            self.player1_turn = 1

    def make_move(self, i):
        
        active_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1

        ########################-DEBUGCODE-############################
        set_probability(active_player)
        set_probability(opponent)
        m1 = best_move(active_player)
        m2 = best_move(opponent)
        print(f"{active_player.name} best move is {m1} {opponent.name} best move is {m2}")
        #########################-DEBUGCODE-#################################

        # set miss "M" or hit "H"
        if i in opponent.indexes:
            active_player.search[i] = "H"
            if hasattr(active_player, "mask"):
                active_player.create_mask(i)
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
            # Change turn
            self.change_turn()
        
        # Check if game over
            game_over = True
            for i in opponent.indexes:
                if active_player.search[i] == "U":
                    game_over = False
            if game_over:
                self.over = 1
                self.winner = active_player



