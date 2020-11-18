import logging
import multiprocessing
import platform

import prompt
import pygame

from LedUpdateProcess import LedUpdateProcess
from LedLine import LedLine
from PyGameLedLine import PyGameLedLine
from algo.LightsAlgo import *

DEFAULT_DELAY = 0.1

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def pygame_init():
  # Initializing Pygame
  pygame.init()

  # Initializing surface
  surface = pygame.display.set_mode((1500, 50))
  surface.fill((0, 0, 0))

  return surface

def leds():
  surface = pygame_init()
  return PyGameLedLine(100, surface)

def algo(line: LedLine):
  return RainbowRunningLight(line)

if __name__ == '__main__':
  if platform.system() == "Darwin":
    multiprocessing.set_start_method('spawn')

  logging.info("Starting PiLights ...")

  queue = multiprocessing.Queue()
  process = LedUpdateProcess(leds, algo, DEFAULT_DELAY, queue)
  process.start()

  while True:
    command = prompt.string()
    if command == 'stop':
      queue.put_nowait('stop')
      process.join()
      break