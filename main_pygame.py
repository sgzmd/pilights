import time
import pygame

from VisualLedLine import VisualLedLine
from LightsAlgo import *


# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((1500, 50))
surface.fill((0, 0, 0))

line = VisualLedLine(200, surface)
algo = RainbowRunningLight(line)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      # quit the game
      pygame.quit()
      quit()

  algo.update()

  line.DisplayLine()
  time.sleep(.005)
  pygame.display.update()

