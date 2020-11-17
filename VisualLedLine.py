import logging
from typing import List

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from LedLine import LedLine

class VisualLedLine(LedLine):
  """
  LedLine which is visualised using PyGame window.
  """
  _surface: Surface = None
  _rects: List[Rect] = []
  _bar_width = 0
  _bar_height = 30

  def __init__(self, size: int, surface: Surface):
    self._surface = surface
    self._bar_width = round(self._surface.get_width() / size)
    self._bar_height = self._surface.get_height()

    for i in range(size):
      rect_x = i * self._bar_width
      rect_y = 0

      self._rects.append(Rect(rect_x,
                              rect_y,
                              self._bar_width,
                              self._bar_height))

    super().__init__(size)

  def DisplayLine(self):
    for i in range(len(self._leds)):
      logging.info("Drawing rectangle {}", i)
      led = self._leds[i]
      bar_color = (255 * led.get_red(), 255 * led.get_green(), 255 * led.get_blue())
      pygame.draw.rect(self._surface, bar_color, self._rects[i])