from PhysicalLedLine import Ws2801LedLine
from algo.RainbowRunningLight import RainbowRunningLight

line = Ws2801LedLine(50)
algo = RainbowRunningLight(line)

while True:
  algo.update()

  line.DisplayLine()
  time.sleep(.05)
