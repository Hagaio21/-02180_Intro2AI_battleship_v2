from game_engine import BattleShipGame
# Pygame setup
import pygame
pygame.init()
pygame.display.set_caption("Battleship")

# Global variables
SQ_SIZE = 20
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH  = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
INDENT = 4

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREY = (30, 50, 60)
GREY2 = (50, 70, 70)
WHITE = (255, 250, 250)
GREEN = (50, 200, 150)
RED = (250,  50, 100)
ORANGE = (250, 140, 20)
COLORS = {"U": GREY, "S": RED, "M": WHITE, "H": ORANGE}

# function that draws a grid
def draw_grid(player, left=0, top=0, search = False):
    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 1)
        if search:
            x += SQ_SIZE//2
            y += SQ_SIZE//2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x,y), radius=SQ_SIZE/4)

# function to draw ships
def draw_ships(Player, left=0, top=0):
    for ship in Player.ships:
        x = left + ship.col * SQ_SIZE + INDENT
        y = top + ship.row * SQ_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size * SQ_SIZE - 2 * INDENT
            height = SQ_SIZE - 2 * INDENT
        else:
            width = SQ_SIZE - 2 * INDENT
            height = ship.size * SQ_SIZE - 2 * INDENT
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius=15)



# Pygame loop:
is_game = True
is_paused = False

game = BattleShipGame()


while is_game:

    # track user interaction.
    for event in pygame.event.get():

        # window close window
        if event.type == pygame.QUIT:
            is_game = False
        
        # user click on mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game.player1_turn and x <  10*SQ_SIZE  and y < 10*SQ_SIZE:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
                
            elif not game.player1_turn and x > WIDTH - 10*SQ_SIZE  and y > 10*SQ_SIZE + V_MARGIN:
                row = (y - 10 * SQ_SIZE - V_MARGIN) // SQ_SIZE
                col = (x - 10 * SQ_SIZE - H_MARGIN) // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
    
            
        # user presses key on keyboard
        if event.type == pygame.KEYDOWN:
            # excape key to close the game:
            if event.key == pygame.K_ESCAPE:
                is_game = False
            
            # spacebar to pause and unpause the game
            if event.key == pygame.K_SPACE:
                is_paused = not(is_paused)

    if not is_paused:

        # draw backgound
        SCREEN.fill(GREY)

        # draw search grids
        draw_grid(game.player1, search=True)
        draw_grid(game.player2, search= True, left = (WIDTH-H_MARGIN) //2 + H_MARGIN, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )

        # draw ship grids
        draw_grid(game.player1, left = (WIDTH-H_MARGIN) //2 + H_MARGIN)
        draw_grid(game.player2, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )
        
        # draw ships onto the ship grids

        draw_ships(game.player1, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )
        draw_ships(game.player2, left = (WIDTH-H_MARGIN) //2 + H_MARGIN)

        # update screen
        pygame.display.flip()
        
pygame.quit()