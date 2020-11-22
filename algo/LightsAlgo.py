from abc import abstractmethod

from colour import Color

from LedLine import LedLine as Line
from algo.OffAlgo import OffAlgo
from algo.RainbowRunningLight import RainbowRunningLight
from algo.RotateLights import RotateLights
from algo.StarryNight import StarryNight
from algo.WhiteRunningLight import WhiteRunningLight

BLACK = Color(rgb=(0, 0, 0))

class LightsAlgo:
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


_algos = [RotateLights, StarryNight, WhiteRunningLight, RainbowRunningLight, OffAlgo]
algo_by_name = {}
for algo in _algos:
  algo_by_name[algo.__name__] = algo

def CreateAlgo(name: str, leds: Line):
  return algo_by_name[name].Create(leds)