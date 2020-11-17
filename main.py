import time
from typing import List

import colour
import pygame
from pygame.locals import *

from LedLine import VisualLedLine as Line

PixelList = List[Color]

def Rainbow():
  line = Line(140)
  seed = 0
  while True:
    for i in range(len(line)):
      line[i] = colour.Color(hsl=((i + 1 + seed) / len(line), 0.5, 0.5))
    line.DisplayLine()
    time.sleep(1)
    if seed == len(line):
      seed = 0
    else:
      seed = seed + 1


if __name__ == '__main__':
  # Initializing Pygame
  pygame.init()

  # Initializing surface
  surface = pygame.display.set_mode((1024, 50))
  line = Line(120, surface)

  surface.fill((0,0,0))

  seed = 0
  while True:
    # getting the events

    # if the event is quit means we clicked on the close window button
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # quit the game
        pygame.quit()
        quit()

    for i in range(len(line)):
      line[i] = colour.Color(hsl=((i + 1 + seed) / len(line), 0.5, 0.5))

    line.DisplayLine()
    if seed == len(line):
      seed = 0
    else:
      seed = seed + 1

    pygame.display.update()
