import math
import random
from abc import ABCMeta, abstractmethod
from collections import deque
from enum import Enum

from colour import Color

from LedLine import LedLine as Line

BLACK = Color(rgb=(0, 0, 0))


class LightAlgo:
  def __init__(self, leds: Line):
    self._leds = leds
    self._len = len(leds)
    self._currentLed = self._len - 1

  @abstractmethod
  def update(self) -> bool:
    """
    Updates the LEDs to their next state.

    :return: True if algorithm is still running and subsequent calls to update() will be processed,
             False if the algorithm has finished the run and now will simply loop.
    """
    pass


class RunningLight(LightAlgo, metaclass=ABCMeta):
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
  _rotateStep = 0

  @abstractmethod
  def nextLightColor(self):
    pass

  def update(self) -> bool:
    if self._rotateStep > 0:
      deq = deque(self._leds.GetLeds())
      deq.rotate(1)
      self._leds.SetLeds(list(deq))
    else:
      self._leds[self._currentLed] = self.nextLightColor()
      if self._currentLed < self._len - 1:
        self._leds[self._currentLed + 1] = BLACK

      self._currentLed = self._currentLed - 1
      if self._currentLed < self._currentStep:
        # Next step
        self._currentLed = self._len - 1
        self._currentStep = self._currentStep + 1

    if self._currentStep == self._len:
      if self._rotateStep == self._len * 3:
        self._currentStep = 0
        self._rotateStep = 0

        # algorithm finished
        return False
      else:
        self._rotateStep = self._rotateStep + 1

    # algorithm can continue
    return True


class RotateLights(LightAlgo, metaclass=ABCMeta):
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
      deq = deque(self._leds.GetLeds())
      deq.rotate(1)
      self._leds.SetLeds(list(deq))
      self._currentStep += 1
      return True
    else:
      self._currentStep = 0
      return False


class WhiteRunningLight(RunningLight):
  @staticmethod
  def Create(leds: Line):
    return WhiteRunningLight(leds)

  """
  Implementation of RunningLight where color(i) is always white
  """

  def nextLightColor(self) -> Color:
    return Color(rgb=(1, 1, 1))


class RainbowRunningLight(RunningLight):
  @staticmethod
  def Create(leds: Line):
    return RainbowRunningLight(leds)

  """
  Implementation of RunningLight where color(i) = next colour in HSL spectrum with H ~ i.
  """

  def __init__(self, leds: Line):
    super().__init__(leds)

  def nextLightColor(self) -> Color:
    hue = (self._currentLed + 1) / self._len
    return Color(hsl=(hue, 1.0, 0.5))


class RotateAndLuminance(LightAlgo):
  class Type(Enum):
    SIN = 0
    RANDOM = 1

  @staticmethod
  def Create(leds: Line):
    return RotateAndLuminance(leds, type = RotateAndLuminance.Type.SIN)

  @staticmethod
  def CreateRandom(leds: Line):
    return RotateAndLuminance(leds, type = RotateAndLuminance.Type.RANDOM)

  _step = 0
  _MAX_STEP = 1000

  def __init__(self, leds: Line, rotate_every=100, type: Type = Type.RANDOM):
    self._rotate_every = rotate_every
    self._type = type
    # Let's fill the line with rainbow colours
    leds.SetLeds([Color(hsl=(i / len(leds), 1.0, 0.5)) for i in range(len(leds))])

    super().__init__(leds)

  def update(self) -> bool:
    # Rotate every 3 steps
    if self._step % self._rotate_every == 0:
      deq = deque(self._leds.GetLeds())
      deq.rotate(1)
      self._leds.SetLeds(list(deq))

    leds = self._leds.GetLeds()
    for i in range(len(leds)):
      luminance = max(
        min(
          abs(self.nextValue(i)),
          0.9),
        0.1)
      color = leds[i]
      color.set_luminance(luminance)
      leds[i] = color
    self._leds.SetLeds(leds)

    self._step += 1
    if self._step > self._MAX_STEP:
      self._step = 0

  def nextValue(self, i):
    if self._type == RotateAndLuminance.Type.SIN:
      return math.sin(math.radians(self._step + i))
    elif self._type == RotateAndLuminance.Type.RANDOM:
      return random.random()

class StarryNight(LightAlgo):
  @staticmethod
  def Create(leds: Line):
    return StarryNight(leds)

  def __init__(self, leds):
    super().__init__(leds)

  def update(self):
    led_index = random.randint(0, len(self._leds) - 1)
    hue = random.randint(0, 360) / 360.0
    luminance = random.randint(0, 90) / 100.0

    self._leds.SetOneLed(
      led_index,
      Color(hsl=(hue, 1.0, luminance)),
      True)
