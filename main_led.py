import time

from PhysicalLedLine import Ws2801LedLine
from LightsAlgo import *

line = Ws2801LedLine(50)
algo = RainbowRunningLight(line)

while True:
  algo.update()

  line.DisplayLine()
  time.sleep(.05)
