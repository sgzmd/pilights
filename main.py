import logging

import prompt

from ConsoleLedLine import ConsoleLedLine
from LedLine import LedLine
from LedUpdateThread import LedUpdateThread
from algo.LightsAlgo import *

DEFAULT_DELAY = 0.1

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def leds():
  return ConsoleLedLine(100)

def start_led_thread(algo, delay = DEFAULT_DELAY) -> LedUpdateThread:
  process = LedUpdateThread(leds, algo, delay)
  return process

if __name__ == '__main__':
  logging.info("Starting PiLights ...")

  algo = RainbowRunningLight.Create
  process = start_led_thread(algo)
  process.start()

  while True:
    command = prompt.string()
    if command == 'stop':
      process.stop()
      logging.info("Stopped LED thread, Ctrl-C for exit.")
    elif command == 'start':
      process.stop()
      process = start_led_thread(algo)
      process.start()
    elif command == 'delay':
      delay = prompt.integer("Delay, ms") / 1000.0
      process.set_delay(delay)
