import time

from LedLine import LedLine as Line
from algo.LightAlgo import LightAlgo

from algo.common import BLACK

class OffAlgo(LightAlgo):
  @staticmethod
  def Create(leds: Line):
    return OffAlgo(leds)

  def __init__(self, leds):
    leds.SetLeds([BLACK for _ in range(len(leds))])
    super().__init__(leds)

  def update(self):
    time.sleep(1)
    pass
