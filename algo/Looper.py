import time

from LedLine import LedLine
from algo.LightAlgo import LightAlgo


class Looper:
  def __init__(self, delay, algo: LightAlgo, line: LedLine):
    self._delay = delay
    self._algo = algo
    self._line = line

  def loop(self):
    while True:
      # Pre-update steps, e.g. erase screen, process PyGame events, etc
      self._line.PreUpdate()() # yes really double parenthesis as PreUpdate returns Callable

      # Update line as passed to algo
      self._algo.update()

      # Display line either on the screen or physical leds
      self._line.DisplayLine()

      # Post update steps, e.g. sending command to update LEDs
      self._line.PostUpdate()() # ditto

      time.sleep(self._delay)
