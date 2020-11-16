import sys
import time
from typing import List

import colour
from colour import Color
from colr import trans, controls

PixelList = List[Color]

class Line:
  _pixels: PixelList = []

  def __init__(self, size):
    self._pixels = [Color(hsl=(0, 0, 0)) for _ in range(size)]

  def __getitem__(self, item):
    return self._pixels[item]

  def __setitem__(self, key, value):
    self.SetColor(key, value)

  def __len__(self):
    return len(self._pixels)

  def SetColor(self, idx: int, pixel: Color):
    assert idx < len(self._pixels)
    self._pixels[idx] = pixel

  def DisplayLine(self):
    controls.erase_display(2)
    for pixel in self._pixels:
      sys.stdout.write('\033[48;5;{code}m \033[0m'.format(code=trans.rgb2term(pixel.get_red() * 255,
                                                                              pixel.get_green() * 255,
                                                                              pixel.get_blue() * 255)))
    sys.stdout.write("\n")


def Rainbow():
  line = Line(140)
  seed = 0
  while True:
    for i in range(len(line)):
      line[i] = colour.Color(hsl=((i + 1 + seed) / len(line), 0.5, 0.5))
    line.DisplayLine()
    time.sleep(0.1)
    if seed == len(line):
      seed = 0
    else:
      seed = seed + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  Rainbow()
