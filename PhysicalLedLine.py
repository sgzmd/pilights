import os.path

if os.path.isfile("/sys/firmware/devicetree/base/model"):
  # Running on Raspberry Pi
  import RPi.GPIO as GPIO
else:
  # Running on Mac maybe
  import RPiSim.GPIO as GPIO

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

from LedLine import LedLine

SPI_PORT = 0
SPI_DEVICE = 0

class Ws2801LedLine(LedLine):
  def __init__(self, size):
    self._pixels = Adafruit_WS2801.WS2801Pixels(size, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
    super().__init__(size)

  def DisplayLine(self):
    for i in range(len(self._leds)):
      led = self._leds[i]
      self._pixels.set_pixel_rgb(i, 255 * led.get_red(), 255 * led.get_green(), 255 * led.get_blue())

    self._pixels.show()