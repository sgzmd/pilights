import math
import random
from collections import deque
from enum import Enum

from colour import Color

from LedLine import LedLine as Line
from algo.LightAlgo import LightAlgo


class RotateAndLuminance(LightAlgo):
  class Type(Enum):
    SIN = 0
    RANDOM = 1

  @staticmethod
  def Create(leds: Line):
    return RotateAndLuminance(leds, type=RotateAndLuminance.Type.SIN)

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
      deq = deque(self._line.GetLeds())
      deq.rotate(1)
      self._line.SetLeds(list(deq))

    leds = self._line.GetLeds()
    for i in range(len(leds)):
      luminance = max(
        min(
          abs(self.nextValue(i)),
          0.9),
        0.1)
      color = leds[i]
      color.set_luminance(luminance)
      leds[i] = color
      self._line.SetOneLed(i, color)

    self._step += 1
    if self._step > self._MAX_STEP:
      self._step = 0

  def nextValue(self, i):
    if self._type == RotateAndLuminance.Type.SIN:
      return math.sin(math.radians(self._step + i))
    elif self._type == RotateAndLuminance.Type.RANDOM:
      return random.random()