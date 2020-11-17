import logging
import pygame

from typing import List
from colour import Color
from pygame import Surface, Rect

class LedLine:
  LedList = List[Color]
  _leds: LedList = []

  def __init__(self, size):
    self._leds = [Color(hsl=(0, 0, 0)) for _ in range(size)]

  def __getitem__(self, item):
    return self._leds[item]

  def __setitem__(self, key, value):
    self._leds[key] = value

  def __len__(self):
    return len(self._leds)

  def GetLeds(self):
    return self._leds

  def DisplayLine(self):
    logging.info("Display line: {}", self._leds)

BG_COLOR = (0, 0, 0)

class VisualLedLine(LedLine):
  _surface: Surface = None
  _rects: List[Rect] = []
  _bar_width = 0
  _bar_height = 30

  def __init__(self, size: int, surface: Surface):
    self._surface = surface
    self._bar_width = self._surface.get_width() / size
    self._bar_height = self._surface.get_height()

    for i in range(size):
      rect_x = i * self._bar_width
      rect_y = 0

      self._rects.append(Rect(rect_x, rect_y, rect_x + self._bar_width, rect_y + self._bar_height))

    super().__init__(size)

  def DisplayLine(self):
    for i in range(len(self._leds)):
      logging.info("Drawing rectangle {}", i)
      led = self._leds[i]
      bar_color = (255 * led.get_red(), 255 * led.get_green(), 255 * led.get_blue())
      pygame.draw.rect(self._surface, bar_color, self._rects[i])

