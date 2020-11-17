from abc import ABCMeta, abstractmethod

from LedLine import LedLine as Line
from colour import Color

BLACK = Color(rgb=(0, 0, 0))


class RunningLight(metaclass=ABCMeta):
  """
  Example of basic RunningLight, relies on abstract nextLightColor implemented.

  color = nextLightColor

  Step 0: all black
  Step 1: LED[n-1] = color(i)
  Step 2: LED[n-1] = black && LED[n-2] = color(i)
  ...
  Step n: LED[1] = black && LED[0] = color(i)

  Step n+1: LED[n-1] = color(i)
  ...
  Step 2*n-1: LED[2] = black&& LED[1] = color(i)
  """
  _currentStep = 0
  _currentLed = 0

  def __init__(self, leds: Line):
    self._leds = leds
    self._len = len(leds)
    self._currentLed = self._len - 1

  @abstractmethod
  def nextLightColor(self):
    pass

  def update(self):
    self._leds[self._currentLed] = self.nextLightColor()
    if self._currentLed < self._len - 1:
      self._leds[self._currentLed + 1] = BLACK

    self._currentLed = self._currentLed - 1
    if self._currentLed < self._currentStep:
      # Next step
      self._currentLed = self._len - 1
      self._currentStep = self._currentStep + 1

    if self._currentStep == self._len:
      self._currentStep = 0


class WhiteRunningLight(RunningLight):
  """
  Implementation of RunningLight where color(i) is always white
  """
  def nextLightColor(self) -> Color:
    return Color(rgb=(1,1,1))

class RainbowRunningLight(RunningLight):
  """
  Implementation of RunningLight where color(i) = next colour in HSL spectrum with H ~ i.
  """
  def __init__(self, leds: Line):
    super().__init__(leds)

  def nextLightColor(self) -> Color:
    hue = (self._currentLed + 1) / self._len
    return Color(hsl=(hue, 1.0, 0.5))