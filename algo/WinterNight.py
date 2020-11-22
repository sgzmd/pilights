from colour import Color

from LedLine import LedLine as Line
from algo import LightsAlgo


class WinterNight(LightsAlgo):
  """
  "Daddy we need something blue".

  OK, blue it is.

  We can start with populating a line worth of blue-ish pixels -
  probably using a colour range from near-green to near-purple.

  Then we start pulsating the brightness using sin.
  """
  def __init__(self, leds: Line):
    super().__init__(leds)

  def update(self):
    pass

