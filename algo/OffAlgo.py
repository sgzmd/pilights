import time

from LedLine import LedLine as Line
from algo import LightsAlgo

class OffAlgo(LightsAlgo):
  @staticmethod
  def Create(leds: Line):
    return OffAlgo(leds)

  def __init__(self, leds):
    leds.SetLeds([LightsAlgo.BLACK for _ in range(len(leds))])
    super().__init__(leds)

  def update(self):
    time.sleep(1)
    pass