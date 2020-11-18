import time
import pygame

from PyGameLedLine import PyGameLedLine
from algo.LightsAlgo import *


# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((1500, 50))
surface.fill((0, 0, 0))

line = PyGameLedLine(50, surface)
algo = RainbowRunningLight(line)

from algo import Looper

def processEvents():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      # quit the game
      pygame.quit()
      quit()

looper = Looper.Looper(processEvents, lambda: pygame.display.update(), 0.01, algo, line)
looper.loop()