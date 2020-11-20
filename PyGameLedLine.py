import time
import logging
from typing import List

import pygame
from colour import Color
from pygame.rect import Rect
from pygame.surface import Surface

from LedLine import LedLine


class PyGameLedLine(LedLine):
  """
  LedLine which is visualised using PyGame window.
  """
  _surface: Surface = None
  _rects: List[Rect] = []
  _bar_width = 0
  _bar_height = 30

  _SMOOTH_STEP = 0.01

  def __init__(self, size: int, surface: Surface):
    self._surface = surface
    self._bar_width = round(self._surface.get_width() / size+1)
    self._bar_height = self._surface.get_height()

    for i in range(size):
      rect_x = i * self._bar_width
      rect_y = 0

      self._rects.append(Rect(rect_x,
                              rect_y,
                              self._bar_width - 5,
                              self._bar_height))

    super().__init__(size)

  def SetOneLed(self, idx: int, color: Color, smooth=False):
    if not smooth:
      super().SetOneLed(idx, color, smooth)
    else:
      lum = self._leds[idx].get_luminance()
      num_steps = round(lum / self._SMOOTH_STEP)

      if lum > 0.1:
        for i in range(num_steps):
          lum -= self._SMOOTH_STEP
          self._leds[idx].set_luminance(lum)
          self.redrawLed(idx)
          self.PreUpdate()
          pygame.display.update()
          time.sleep(0.01)

      new_lum = 0
      num_steps = round(color.get_luminance() / self._SMOOTH_STEP)
      for i in range(num_steps - 1):
        # we start with a non-zero value
        new_lum += self._SMOOTH_STEP
        color.set_luminance(new_lum)
        self._leds[idx] = color
        self.redrawLed(idx)
        self.PreUpdate()
        pygame.display.update()
        time.sleep(0.01)

    super().SetOneLed(idx, color)

  def DisplayLine(self):
    for i in range(len(self._leds)):
      led = self._leds[i]
      bar_color = self.toPyGameColor(led)
      pygame.draw.rect(self._surface, bar_color, self._rects[i])

  def toPyGameColor(self, led):
    bar_color = (255 * led.get_red(), 255 * led.get_green(), 255 * led.get_blue())
    return bar_color

  def redrawLed(self, idx):
    pygame.draw.rect(self._surface,
                     self.toPyGameColor(self._leds[idx]),
                     self._rects[idx])

  def PreUpdate(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # quit the game
        pygame.quit()
        quit()

  def PostUpdate(self):
    pygame.display.update()
