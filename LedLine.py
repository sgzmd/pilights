from abc import ABCMeta, abstractmethod

from typing import List, Callable
from colour import Color

class LedLine(metaclass=ABCMeta):
  """
  Abstract LedLine without any visualisation, relies on abstract DisplayLine being implemented.
  """
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

  def SetLeds(self, leds: LedList):
    self._leds = leds

  @abstractmethod
  def DisplayLine(self):
    pass

  @abstractmethod
  def PreUpdate(self) -> Callable:
    pass

  @abstractmethod
  def PostUpdate(self) -> Callable:
    pass


BG_COLOR = (0, 0, 0)

