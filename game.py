# Importing the library
import pygame
import sys

from pygame.locals import *

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((1024, 768))

# Initialing Color
color = (255, 0, 0)

# Drawing Rectangle
pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60))

while True:
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      sys.exit(0)