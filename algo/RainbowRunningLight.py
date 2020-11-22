from colour import Color

from LedLine import LedLine as Line
from algo.RunningLight import RunningLight


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