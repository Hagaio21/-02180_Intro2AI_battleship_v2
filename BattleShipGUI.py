from game_engine import BattleShipGame
# Pygame setup
import pygame
import time
pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
FONT = pygame.font.SysFont("fresansttf", 80)
# Global variables
SQ_SIZE = 20
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH  = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
INDENT = 4

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREY = (30, 42, 52)
GREY2 = (50, 70, 70)
WHITE = (255, 250, 250)
GREEN = (50, 200, 150)
RED = (250,  50, 100)
BLUE = (0, 150, 150)
ORANGE = (255, 150, 20)
COLORS = {"U": GREY, "S": RED, "M": BLUE, "H": ORANGE}
# helper functions 

def value_to_brg_heatmap(value, min_value=0, max_value=100):
    # Normalize the value
    normalized = (value - min_value) / (max_value - min_value)
    return (int(normalized * 255), int(normalized * 255), int(normalized * 255))

# function that draws a grid
def draw_grid(player, left=0, top=0, search = False, mask = False):
    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 1)
        if mask:
            if hasattr(player,"mask"):
                square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
                color = value_to_brg_heatmap(player.probability[i]+player.mask[i],
                                             min_value=min(player.probability) + min(player.mask),
                                             max_value=max(player.probability) +max(player.mask))
                pygame.draw.rect(SCREEN, color, square)
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
ai_mask = False
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
        # user presses key on keyboard
        if event.type == pygame.KEYDOWN:
            # excape key to close the game:
            if event.key == pygame.K_ESCAPE:
                is_game = False
            
            # spacebar to pause and unpause the game
            if event.key == pygame.K_SPACE:
                is_paused = not(is_paused)
            
            # return key to restart the game
            if event.key == pygame.K_RETURN:
                game = BattleShipGame()
            
            # toggle ai grid mask
            if event.key == pygame.K_m:
                ai_mask = not ai_mask

    if not game.player1_turn:
        game.make_move(game.player2.AI_move())
        time.sleep(0.5)
            
            # elif not game.player1_turn and x > WIDTH - 10*SQ_SIZE  and y > 10*SQ_SIZE + V_MARGIN:
            #     row = (y - 10 * SQ_SIZE - V_MARGIN) // SQ_SIZE
            #     col = (x - 10 * SQ_SIZE - H_MARGIN) // SQ_SIZE
            #     index = row * 10 + col
            #     game.make_move(index)
    
            

    if not is_paused:

        # draw backgound
        SCREEN.fill(GREY)

        # draw search grids
        draw_grid(game.player1, search=True)
        draw_grid(game.player2, search= True,mask=ai_mask, left = (WIDTH-H_MARGIN) //2 + H_MARGIN, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )
    
        # draw ship grids
        draw_grid(game.player1, left = (WIDTH-H_MARGIN) //2 + H_MARGIN)
        draw_grid(game.player2, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )
        
        # draw ships onto the ship grids

        draw_ships(game.player1, top = (HEIGHT-V_MARGIN) //2 + V_MARGIN )
        draw_ships(game.player2, left = (WIDTH-H_MARGIN) //2 + H_MARGIN)

        # game over message
        if game.over == 1:
            text = f"{game.winner.name} won!"
            textbox = FONT.render(text, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 -225, HEIGHT//2 - 50))


        # update screen
        pygame.display.flip()

game.player2.save_AI_log()
pygame.quit()