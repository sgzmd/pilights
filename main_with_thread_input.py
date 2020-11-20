import enum
import logging
import queue
import sys
import threading
import time

import click
import prompt

from LedLine import LedLine
from algo import LightsAlgo

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')

class ControlMessage:
  class MessageType(enum.Enum):
    STOP = 1
    CHANGE_DELAY = 2
    CHANGE_ALGO = 3

  _data = None
  _messageType: MessageType = None

  def __init__(self, type: MessageType, data = None):
    self._messageType = type
    self._data = data

  def type(self):
    return self._messageType

  def set_data(self, data):
    self._data = data

  def data(self):
    return self._data

class ControlThread(threading.Thread):
  def __init__(self, q: queue.Queue):
    self._q = q
    super().__init__()

  def run(self) -> None:
    while True:
      command = prompt.string("Enter command (stop/delay/algo): ")
      if command == 'stop':
        logging.info("Stopping the program")
        self._q.put_nowait(ControlMessage(ControlMessage.MessageType.STOP))
        return
      elif command == 'algo':
        algo_names = ", ".join(LightsAlgo.algo_by_name.keys())
        new_algo_name = prompt.string(f"Select new algorithm, one of {algo_names}: ")
        logging.info("Requesting algorithm change to %s", new_algo_name)

        self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_ALGO,
          new_algo_name))

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

  q = queue.Queue(1)
  control_thread = ControlThread(q)
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
        algo = LightsAlgo.CreateAlgo(event.data(), line)

    line.PreUpdate()
    algo.update()
    line.DisplayLine()
    line.PostUpdate()
    sleep(mode, delay)


if __name__ == '__main__':
  run()
