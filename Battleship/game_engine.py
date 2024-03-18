# Game Engine
import random

####### GLOBAL VARIABLES #############################################

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

####### GLOBAL VARIABLES END ##########################################

###### AI PLAYER HELPER FUNCTIONS START ###############################

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

def set_mask(player):
    update_indexes = []
    if not hasattr(player, "mask"):
        player.mask = [*range(100)]
    else:
        for index ,value in enumerate(player.search):
            if value == "M" or value == "H" or value == "S":
                update_indexes.append(index)
    for index in update_indexes:
        player.mask[index] = 0


# Heuristic function for choosing the best next move
# The Heuristic function asign a value to the the AI can take     
def heuristic(player, move):
    p = player
    m = move
    if hasattr(p, 'mask'):
        h = p.probability[m] + p.mask[m]
    else:
        return 0
    return h

# the best move function compare heuristics of all the moves,
# then return the best move (move with the highest heuristic value)
def best_move(player):
    best_m = player.moves[0]
    best_h = 0
    for m in player.moves:
        # compare heuristics
        if  heuristic(player, m) > heuristic(player, best_m):
            best_m = m
        elif heuristic(player, m) == heuristic(player, best_m):
            result = random.randint(0, 1)
            if result == 0:
                best_m = m

    return best_m

###### AI PLAYER HELPER FUNCTIONS END ###############################
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



################### AI PLAYER CODE START ###########################
class AIPlayer(Player):
   
    # Initiate AI player with relevant mode
    def AI_init(self, mode):
            # Innitiate AI player attibutes
            self.probability = START_PROBABILITY
            self.mask = [0 for i in range(100)]
            self.mode = mode
            self.turn = 0
            self.log = []
            self.is_zeroing_on_a_ship = "no"
            self.last_move_result = ""
            self.last_move_location = []
            self.mask_flag = 0
            

    # function that log states of AI.
    def AI_log_state(self):
        self.log.append({'probabilty': self.probability, 'mask': self.mask, 'moves': self.moves})

    # Logging fuction that saves all of the AI player states to an external file
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

    # AI move function
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

    def make_move_AI(self):
        if self.is_zeroing_on_a_ship == "yes":
            pass
        elif self.is_zeroing_on_a_ship == 'no':
            pass 


    #mask works but only assigns ones
    
    # creates mask of values for the new search grid

    def create_mask(self, i):
        if self.mask_flag == 0:
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
            # raise created mask flag
            self.mask_flag = 1 
        # if there's already a mask, behave like this...:
        elif self.mask_flag == 1:
            pass
    
    def reset_mask(self):
        self.mask_flag = 0
        self.mask = [0 for i in  range(100)]
    
    def update_mask(self, i):
        for i, indicies in enumerate(self.search):
            if indicies == "M":
        
                row_index = i // 10
                col_index = i % 10
                
                # Check right neighbor
                if col_index < 9 and self.search[i+1] == "H":
                    for j in range(row_index * 10, i):
                        self.mask[j] = 0 
                        
                # Check left neighbor
                if col_index > 0 and self.search[i-1] == "H":
                    for j in range(i, (row_index + 1) * 10):
                        self.mask[j] = 0 
                        
                # Check bottom neighbor
                if row_index < 9 and self.search[i+10] == "H":
                    for j in range(col_index, i, 10):
                        self.mask[j] = 0 
                        
                # Check top neighbor
                if row_index > 0 and self.search[i-10] == "H":
                    for j in range(i, 100, 10):
                        self.mask[j] = 0
        


################### AI PLAYER CODE END ###############################
class BattleShipGame():

    def __init__(self):
        self.player1 = Player("Player1")
        self.player2 = AIPlayer("AI")
        self.player2.AI_init(mode='H1')
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


        # set miss "M" or hit "H"
        if i in opponent.indexes:
            active_player.search[i] = "H"

            ###############################
            print("HIT!")
            result = "H"
            ###############################
            # check if ship is sunk ("S")
            for ship in opponent.ships:
                sunk = True # assume ship is sunk
                for j in ship.indexes:
                    if active_player.search[j] == "U":
                        sunk = False
                        break
                if sunk:
                    for j in ship.indexes:
                        active_player.search[j] = "S"
        else:
            active_player.search[i] = "M"
            # Change turn if misses
            self.change_turn()

        # save the move result
            
        result = active_player.search[i]
        ########################
        print(result)
        ########################
        # check what to do next -- only for AI player
        if active_player.name == "AI":
            
            ####################################
            print(f"result is {result}, AI mask flag is {active_player.mask_flag}")
            ###################################
            if result == "H":
                active_player.create_mask(i)
            if result == "S":
                active_player.reset_mask()
            if result == "M":
                pass
            active_player.update_mask(i)
            
        
        # Check if game over
        game_over = True
        for i in opponent.indexes:
            if active_player.search[i] == "U":
                game_over = False
        if game_over:
            self.over = 1
            self.winner = active_player


