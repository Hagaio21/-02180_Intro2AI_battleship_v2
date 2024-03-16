from game_engine import BattleShipGame
# Pygame setup
import pygame
pygame.init()
pygame.display.set_caption("Battleship")
import time

game = BattleShipGame()

x = game.player2._create_mask()
a = game.player2.create_mask(35)
for i in range(100):
        print(a[i], end = " ")
print(' ')
        
