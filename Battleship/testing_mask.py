from game_engine import BattleShipGame
# Pygame setup
import pygame
pygame.init()
pygame.display.set_caption("Battleship")
import time

game = BattleShipGame()

x = game.player2._create_mask()
a = game.player2.create_mask(35)
# for i in range(100):
#         print(a[i], end = " ")
# print(' ')
        
counter = 0
for i in range(10):
    for j in range(10):
        print(a[counter], end = " ")
        counter += 1
    print(' ')
