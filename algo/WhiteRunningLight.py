from colour import Color

from LedLine import LedLine as Line
from algo.RunningLight import RunningLight


class WhiteRunningLight(RunningLight):
  @staticmethod
  def Create(leds: Line):
    return WhiteRunningLight(leds)

  """
  Implementation of RunningLight where color(i) is always white
  """

  def nextLightColor(self) -> Color:
    return Color(rgb=(1, 1, 1))