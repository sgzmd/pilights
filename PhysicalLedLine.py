import os.path
import time

from colour import Color

if os.path.isfile("/sys/firmware/devicetree/base/model"):
  # Running on Raspberry Pi
  RUNNING_ON_PI = True
else:
  # Running on Mac maybe
  GPIO = None
  RUNNING_ON_PI = False

import board
import adafruit_ws2801

from LedLine import LedLine

DEBUG = True or not RUNNING_ON_PI
if DEBUG:
  pass

SPI_PORT = 0
SPI_DEVICE = 0


def to_physical_color(color, adjust=1.0):
  return (int(round(255 * color.get_red() * adjust)),
          int(round(255 * color.get_green() * adjust)),
          int(round(255 * color.get_blue()) * adjust))


class Ws2801LedLine(LedLine):
  _pixels : adafruit_ws2801.WS2801 = None

  def __init__(self, size):
    if RUNNING_ON_PI:
      self._pixels = adafruit_ws2801.WS2801(board.D11, board.D10, size, auto_write = False)
    super().__init__(size)
    self._leds = [Color(rgb=(0,0,0)) for _ in range(len(self._leds))]

    self.DisplayLine()

  def DisplayLine(self):
    for i in range(len(self._leds)):
      led = self._leds[i]
      if RUNNING_ON_PI:
        # self._pixels[i] = (round(255 * led.get_red()), round(255 * led.get_green()), round(255 * led.get_blue()))
        self.SetOneLed(i, led)
    self._pixels.show()

  def SetOneLed(self, idx: int, color: Color, smooth=False):
    self._leds[idx] = color
    if not smooth:
      self._pixels[idx] = to_physical_color(color)
    else:
      for i in range(10):
        adjust = (i+1) / 10.0
        self._pixels[idx] = to_physical_color(color, adjust)
        self._pixels.show()
        time.sleep(0.01)

  def PostUpdate(self):
    self._pixels.show()

  def SetBrightness(self, brightness: float):
    self._pixels.brightness = brightness
    self._pixels.show()
