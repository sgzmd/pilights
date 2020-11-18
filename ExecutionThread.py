import logging
import multiprocessing
import time

from LedLine import LedLine
from algo.LightsAlgo import LightAlgo

class ExecutionThread(multiprocessing.Process):
  _stop = False
  _line: LedLine = None
  _algo: LightAlgo = None

  def __init__(self, line: LedLine, algo: LightAlgo, delay: float, queue: multiprocessing.Queue):
    self._lineFactory = line
    self._algoFactory = algo
    self._delay = delay
    self._queue = queue
    super().__init__()

  def stop(self):
    _stop = True

  def run(self):
    logging.info("Starting Looper thread ... ")
    self._line = self._lineFactory()
    self._algo = self._algoFactory(self._line)
    while True:
      if not self._queue.empty() and self._queue.get_nowait() == 'stop':
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