import time
from typing import List

import colour
import pygame

from LedLine import VisualLedLine
from PhysicalLedLine import Ws2801LedLine
from LightsAlgo import *

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

def MovingRainbow(surface: pygame.Surface):
  # line = VisualLedLine(50, surface)
  line = Ws2801LedLine(50)
  start_color = 0
  start_bright = len(line)

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

    if start_color == len(line):
      start_color = 0
      start_bright = len(line)
    else:
      start_color = start_color + 1
      start_bright = start_bright - 1

if __name__ == '__main__':
  # Initializing Pygame
  pygame.init()

  # Initializing surface
  surface = pygame.display.set_mode((1000, 50))
  surface.fill((0,0,0))

  MovingRainbow(surface)