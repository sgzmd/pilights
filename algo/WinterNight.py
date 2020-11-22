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
    super().__init__(line)
    self._start = Color(hsl=(248/360.0, 1, 0.13))
    self._end = Color(hsl=(176/360.0, 1, 0.72))

    self._range = list(self._start.range_to(self._end, len(line)))
    pass

  def update(self) -> bool:
    if self._step <  self._len:
      self._line[self._step] = self._range[self._step]
      self._step += 1
    else:
      self._line = [BLACK for _ in range(self._len)]
      pass
