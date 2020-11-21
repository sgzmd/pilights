import os.path
import sys
from colour import Color

if os.path.isfile("/sys/firmware/devicetree/base/model"):
  # Running on Raspberry Pi
  import RPi.GPIO as GPIO
  RUNNING_ON_PI = True
else:
  # Running on Mac maybe
  GPIO = None
  RUNNING_ON_PI = False

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

from LedLine import LedLine

DEBUG = True or not RUNNING_ON_PI
if DEBUG:
  from colr import trans, controls

SPI_PORT = 0
SPI_DEVICE = 0

class Ws2801LedLine(LedLine):
  def __init__(self, size):
    if RUNNING_ON_PI:
      self._pixels = Adafruit_WS2801.WS2801Pixels(
          size, 
          spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
    self._leds = [Color(rgb=(0,0,0) for _ in range(len(self._leds)))]
    super().__init__(size)
    self.DisplayLine()

  def DisplayLine(self):
    for i in range(len(self._leds)):
      led = self._leds[i]
      if RUNNING_ON_PI:
        self._pixels.set_pixel_rgb(i,
          round(255 * led.get_red()),
          round(255 * led.get_green()),
          round(255 * led.get_blue()))

    if RUNNING_ON_PI:
      self._pixels.show()

    if DEBUG:
      controls.erase_display(2)
      for pixel in self._leds:
        sys.stdout.write('\033[48;5;{code}m \033[0m'.format(code=trans.rgb2term(pixel.get_red() * 255,
                                                                                pixel.get_green() * 255,
                                                                                pixel.get_blue() * 255)))
      sys.stdout.write("\n")