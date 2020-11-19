import logging

import prompt

from LedUpdateThread import LedUpdateThread
from algo.LightsAlgo import *

DEFAULT_DELAY = 0.1

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
USE_DUMMY_THREADING = True

def leds():
  import pygame
  from PyGameLedLine import PyGameLedLine
  pygame.init()
  surface = pygame.display.set_mode((1500, 50))
  surface.fill((0, 0, 0))

  return PyGameLedLine(100, surface)

def start_led_thread(algo, delay = DEFAULT_DELAY) -> LedUpdateThread:
  process = LedUpdateThread(leds, algo, delay)
  return process

if __name__ == '__main__':
  logging.info("Starting PiLights ...")

  algo = RotateAndLuminance.Create
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
      delay = prompt.integer("Delay, ms: ") / 1000.0
      if not USE_DUMMY_THREADING:
        process.set_delay(delay)
      else:
        process.stop()
        process = start_led_thread(algo)
        process.set_delay(delay)
        process.start()
    elif command == 'algo':
      algo_name = prompt.string("New algo name: white/rainbow/rotate/lum: ")
      if algo_name == 'white':
        algo = WhiteRunningLight.Create
      elif algo_name == 'rainbow':
        algo = RainbowRunningLight.Create
      elif algo_name == 'rotate':
        algo = RotateLights.Create
      elif algo_name == 'lum':
        algo = RotateAndLuminance.Create
      else:
        logging.error("Unrecognised algo %s", algo_name)
        continue

      process.stop()
      process = start_led_thread(algo)
      process.start()
    else:
      logging.error("Unrecognised command: %s", command)

