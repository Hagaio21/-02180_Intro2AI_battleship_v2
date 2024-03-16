from game_engine import BattleShipGame
# Pygame setup
import pygame
pygame.init()
pygame.display.set_caption("Battleship")
import time

game = BattleShipGame()

x = game.player2._create_mask()
a = game.player2.create_mask(10)
for i in range(10):
    for j in range(10):
        print(a[j], end = 0)
    print(' ')
        
