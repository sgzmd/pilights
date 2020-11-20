import logging
import time

import click
import threading

import prompt

from algo import LightsAlgo

from LedLine import LedLine

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')
# def UpdateThreadFunction(algo: LightsAlgo.LightAlgo):
#   while True:
#     command = prompt.string()
#     if command == 'delay':
#       delay = prompt.integer("Delay, ms: ") / 1000.0
#
#     elif command == 'algo':
#       algo_name = prompt.string("New algo name: white/rainbow/rotate/lum: ")
#       if algo_name == 'white':
#         algo = WhiteRunningLight.Create
#       elif algo_name == 'rainbow':
#         algo = RainbowRunningLight.Create
#       elif algo_name == 'rotate':
#         algo = RotateLights.Create
#       elif algo_name == 'lum':
#         algo = RotateAndLuminance.Create
#       elif algo_name == 'night':
#         algo = StarryNight.Create
#       else:
#         logging.error("Unrecognised algo %s", algo_name)
#         continue
#
#       process.stop()
#       process = start_led_thread(algo)
#       process.start()
#     else:
#       logging.error("Unrecognised command: %s", command)

def sleep(mode: str, delay: int):
  if mode == "pygame":
    import pygame
    pygame.time.delay(delay)
  elif mode in ("console", "led"):
    time.sleep(delay)
  else:
    raise ValueError(f"Mode {mode} is not supported")


@click.command()
@click.option("--mode", default="pygame", help="Mode to launch in (console/pygame/led)")
@click.option("--num", default=50, help="Number of leds")
@click.option("--algo", default="StarryNight", help="Name of the initial algorithm")
@click.option("--delay", default=100, help="Delay, ms")
def run(mode: str, num: int, algo: str, delay: int):
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

  algo = LightsAlgo.CreateAlgo(algo, line)

  while True:
    line.PreUpdate()
    algo.update()
    line.DisplayLine()
    line.PostUpdate()
    sleep(mode, delay)


if __name__ == '__main__':
  run()
