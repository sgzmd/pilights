import logging
import queue
import sys
import time

import click

from LedLine import LedLine
from algo import algos
from control.message import ControlMessage
from control.web import WebControlThread

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')


def sleep(mode: str, delay: int):
  if mode == "pygame":
    import pygame
    pygame.time.delay(delay)
  elif mode in ("console", "led"):
    time.sleep(delay / 100.0)
  else:
    raise ValueError(f"Mode {mode} is not supported")

def log_delay(speed: int) -> int:
  """
  Computes logarithmic delay. The higher the speed is, the more should be the increase of
  the speed to make it more noticeable, the slower it is the less should be the increase
  to allow for fine control.

  with speed changing [1, 100] (the higher the faster) delay is inverse proportional to the
  speed and can be calculated as:
  :param speed:
  :return:
  """


@click.command()
@click.option("--mode", default="led", help="Mode to launch in (console/pygame/led)")
@click.option("--num", default=96, help="Number of leds")
@click.option("--algo", default="StarryNight", help="Name of the initial algorithm")
@click.option("--delay", default=100, help="Delay, ms")
@click.option("--apikey", default="", help="Telegram API key")
def run(mode: str, num: int, algo: str, delay: int, apikey: str):
  logging.info("Starting main thread with mode %s", mode)

  line: LedLine = None
  if mode == "pygame":
    from PyGameLedLine import PyGameLedLine
    import pygame
    pygame.init()

    # Initializing surface
    surface = pygame.display.set_mode((1500, 50))
    surface.fill((0, 0, 0))

    line = PyGameLedLine(num, surface)
  elif mode == "led":
    from PhysicalLedLine import Ws2801LedLine
    line = Ws2801LedLine(num)
  elif mode == "console":
    from ConsoleLedLine import ConsoleLedLine
    line = ConsoleLedLine(num)

  algo = algos.CreateAlgo(algo, line)

  q = queue.Queue(1)
  control_thread = WebControlThread(q, delay)
  control_thread.start()
  while True:
    if not q.empty():
      event : ControlMessage = q.get_nowait()
      if event.type() == ControlMessage.MessageType.STOP:
        logging.info("Received STOP message, exiting ... ")
        sys.exit(0)
      elif event.type() == ControlMessage.MessageType.CHANGE_ALGO:
        logging.info("Changing algo to %s", event.data())
        line.ClearLine()
        algo = algos.CreateAlgo(event.data(), line)
      elif event.type() == ControlMessage.MessageType.CHANGE_DELAY:
        logging.info("Changing delay to %d", event.data())
        delay = event.data()
      elif event.type() == ControlMessage.MessageType.CHANGE_BRIGHTNESS:
        logging.info("Changing brightness to %f", event.data())
        line.SetBrightness(event.data())

    line.PreUpdate()
    algo.update()
    line.DisplayLine()
    line.PostUpdate()
    sleep(mode, delay)

if __name__ == '__main__':
  run()
