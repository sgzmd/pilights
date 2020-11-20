import enum
import logging
import queue
import threading

import prompt
from algo import LightsAlgo

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
      elif command == 'delay':
        new_delay = prompt.integer("Enter new delay, ms: ")
        self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_DELAY,
          new_delay))