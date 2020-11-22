from abc import ABCMeta, abstractmethod
from collections import deque

from algo.LightsAlgo import LightsAlgo, BLACK


class RunningLight(LightsAlgo, metaclass=ABCMeta):
  """
  Example of basic RunningLight, relies on abstract nextLightColor implemented.

  color = nextLightColor

  Step 0: all black
  Step 1: LED[n-1] = color(i)
  Step 2: LED[n-1] = black && LED[n-2] = color(i)
  ...
  Step n: LED[1] = black && LED[0] = color(i)

  Step n+1: LED[n-1] = color(i)
  ...
  Step 2*n-1: LED[2] = black&& LED[1] = color(i)
  """
  _currentStep = 0
  _currentLed = 0
  _rotateStep = 0

  @abstractmethod
  def nextLightColor(self):
    pass

  def update(self) -> bool:
    if self._rotateStep > 0:
      deq = deque(self._line.GetLeds())
      deq.rotate(1)
      self._line.SetLeds(list(deq))
    else:
      self._line[self._currentLed] = self.nextLightColor()
      if self._currentLed < self._len - 1:
        self._line[self._currentLed + 1] = BLACK

      self._currentLed = self._currentLed - 1
      if self._currentLed < self._currentStep:
        # Next step
        self._currentLed = self._len - 1
        self._currentStep = self._currentStep + 1

    if self._currentStep == self._len:
      if self._rotateStep == self._len * 3:
        self._currentStep = 0
        self._rotateStep = 0

        # algorithm finished
        return False
      else:
        self._rotateStep = self._rotateStep + 1

    # algorithm can continue
    return True