from LedLine import LedLine as Line
from algo.OffAlgo import OffAlgo
from algo.RainbowRunningLight import RainbowRunningLight
from algo.RotateLights import RotateLights
from algo.StarryNight import StarryNight
from algo.WhiteRunningLight import WhiteRunningLight

_algos = [RotateLights, StarryNight, WhiteRunningLight, RainbowRunningLight, OffAlgo]
algo_by_name = {}
for algo in _algos:
  algo_by_name[algo.__name__] = algo


def CreateAlgo(name: str, leds: Line):
  return algo_by_name[name].Create(leds)
