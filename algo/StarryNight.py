import random

from colour import Color

from LedLine import LedLine as Line
from algo.LightsAlgo import LightsAlgo


class StarryNight(LightsAlgo):
  @staticmethod
  def Create(leds: Line):
    return StarryNight(leds)

  def __init__(self, leds):
    super().__init__(leds)

  def update(self):
    led_index = random.randint(0, len(self._line) - 1)
    hue = random.randint(0, 360) / 360.0
    luminance = random.randint(0, 90) / 100.0

    self._line.SetOneLed(
      led_index,
      Color(hsl=(hue, 1.0, luminance)),
      True)