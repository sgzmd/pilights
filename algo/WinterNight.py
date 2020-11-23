from collections import deque
from colour import Color

from LedLine import LedLine as Line
from algo.LightAlgo import LightAlgo
from algo.common import BLACK

class WinterNight(LightAlgo):
  _step: int = 0

  @staticmethod
  def Create(line: Line):
    return WinterNight(line)

  def __init__(self, line: Line):
    self._start = Color(hsl=(248/360.0, 1, 0.13))
    self._end = Color(hsl=(176/360.0, 1, 0.72))
    self._iteration = 0
    half_len = round(len(line) / 2)
    self._range = list(self._start.range_to(self._end, half_len))
    for element in reversed(self._range):
      self._range.append(element)
    if len(line) % 2 != 0:
      self._range.append(self._range[1])
    super().__init__(line)

  def update(self) -> bool:
    if self._step <  self._len:
      self._line[self._step] = self._range[self._step]
      self._step += 1
    else:
      deq = deque(self._line.GetLeds())
      deq.rotate(-1)
      self._line.SetLeds(list(deq))

      if self._step < (2+self._iteration % 3 + 0.2)*self._len:
        self._step += 1
      else:
        self._step = 0
        self._iteration += 1
        if self._iteration > 999:
          self._iteration = 0


