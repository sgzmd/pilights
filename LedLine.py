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
    self.PreUpdate()
    self._leds = leds
    self.PostUpdate()

  def SetOneLed(self, idx: int, color: Color, smooth = False):
    self._leds[idx] = color

  @abstractmethod
  def DisplayLine(self):
    pass

  def PreUpdate(self) -> Callable:
    pass

  def PostUpdate(self) -> Callable:
    pass

  def ClearLine(self):
    num_leds = len(self._leds)
    self._leds = [Color(rgb=(0,0,0)) for _ in range(num_leds)]
    self.DisplayLine()


  def SetBrightness(self, brightness: float):
    pass


BG_COLOR = (0, 0, 0)

