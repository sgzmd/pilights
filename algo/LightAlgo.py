from abc import abstractmethod
from LedLine import LedLine as Line

class LightAlgo:
  def __init__(self, leds: Line):
    self._line = leds
    self._len = len(leds)
    self._currentLed = self._len - 1

  @abstractmethod
  def update(self) -> bool:
    """
    Updates the LEDs to their next state.

    :return: True if algorithm is still running and subsequent calls to update() will be processed,
             False if the algorithm has finished the run and now will simply loop.
    """
    pass