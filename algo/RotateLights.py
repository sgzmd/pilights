from abc import ABCMeta
from collections import deque

from colour import Color

from LedLine import LedLine as Line
from algo.LightsAlgo import LightsAlgo


class RotateLights(LightsAlgo, metaclass=ABCMeta):
  _currentStep = 0

  @staticmethod
  def Create(leds: Line):
    return RotateLights(leds)

  def __init__(self, leds: Line, times=None):
    self._rotateTimes = times

    # Let's fill the line with rainbow colours
    leds.SetLeds([Color(hsl=(i / len(leds), 1.0, 0.5)) for i in range(len(leds))])

    super().__init__(leds)

  def update(self) -> bool:
    if not self._rotateTimes or self._currentStep < self._rotateTimes:
      deq = deque(self._line.GetLeds())
      deq.rotate(1)
      self._line.SetLeds(list(deq))
      self._currentStep += 1
      return True
    else:
      self._currentStep = 0
      return False