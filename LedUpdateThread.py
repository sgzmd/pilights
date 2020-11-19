import logging
import threading
import time

from LedLine import LedLine
from algo.LightsAlgo import LightAlgo

class LedUpdateThread(threading.Thread):
  _stop = False
  _line: LedLine = None
  _algo: LightAlgo = None

  def __init__(self, line: LedLine, algo: LightAlgo, delay: float):
    self._lineFactory = line
    self._algoFactory = algo
    self._delay = delay
    super().__init__()

  def stop(self):
    self._stop = True

  def set_delay(self, delay: float):
    self._delay = delay

  def run(self):
    logging.info("Starting Looper thread ... ")
    self._line = self._lineFactory()
    self._algo = self._algoFactory(self._line)
    while True:
      if self._stop:
        break

      # Pre-update steps, e.g. erase screen, process PyGame events, etc
      self._line.PreUpdate()()  # yes really double parenthesis as PreUpdate returns Callable

      # Update line as passed to algo
      self._algo.update()

      # Display line either on the screen or physical leds
      self._line.DisplayLine()

      # Post update steps, e.g. sending command to update LEDs
      self._line.PostUpdate()()  # ditto

      time.sleep(self._delay)