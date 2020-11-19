import logging
import sys
from typing import List

from colr import trans, controls
from LedLine import LedLine

class ConsoleLedLine(LedLine):
  """
  LedLine which is visualised using console.
  """
  _bar_width = 0
  _bar_height = 30


  def __init__(self, size: int):
    super().__init__(size)

  def DisplayLine(self):
    for pixel in self._leds:
      sys.stdout.write('\033[48;5;{code}m \033[0m'.format(code=trans.rgb2term(pixel.get_red() * 255,
                                                                              pixel.get_green() * 255,
                                                                              pixel.get_blue() * 255)))
    sys.stdout.write("\n")

  def PreUpdate(self):
    def pre_update():
      controls.erase_display(2)

    return pre_update

  def PostUpdate(self):
    def post_update():
      pass

    return post_update
