from LedLine import LedLine as Line
from algo.OffAlgo import OffAlgo
from algo.RainbowRunningLight import RainbowRunningLight
from algo.RotateLights import RotateLights
from algo.StarryNight import StarryNight
from algo.WhiteRunningLight import WhiteRunningLight
from algo.WinterNight import WinterNight

_algos = [RotateLights, StarryNight, WhiteRunningLight, RainbowRunningLight, OffAlgo, WinterNight]
algo_by_name = {}
for algo in _algos:
  algo_by_name[algo.__name__] = algo

def GetAlgos():
  return _algos

def CreateAlgo(name: str, leds: Line):
  return algo_by_name[name].Create(leds)
