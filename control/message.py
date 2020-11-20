import enum


class ControlMessage:
  class MessageType(enum.Enum):
    STOP = 1
    CHANGE_DELAY = 2
    CHANGE_ALGO = 3

  _data = None
  _messageType: MessageType = None

  def __init__(self, type: MessageType, data=None):
    self._messageType = type
    self._data = data

  def type(self):
    return self._messageType

  def set_data(self, data):
    self._data = data

  def data(self):
    return self._data