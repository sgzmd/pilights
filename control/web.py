import logging
import os
import queue
import threading

from control.message import ControlMessage

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')

from flask import Flask, render_template, redirect

templates = os.path.abspath(os.path.dirname(__file__) + "/../templates")
logging.info("Flask will be looking for templates in %s", templates)
app = Flask(__name__, template_folder=templates)

control_queue: queue.Queue = None

MAX_DELAY = 1000
MIN_DELAY = 1
DELAY_STEP = 100


class SpeedControl():
  def __init__(self, initial_speed: int):
    self._initial_speed = initial_speed
    self._delay = initial_speed

  def faster(self):
    if self._delay < MIN_DELAY:
      return False
    else:
      self._delay -= DELAY_STEP
      return True

  def slower(self):
    if self._delay > MAX_DELAY:
      return False
    else:
      self._delay += DELAY_STEP
      return True

  def delay(self):
    return self._delay

delay: SpeedControl = None


algos = {
  "starry_night": "StarryNight",
  "rainbow": "RotateLights",
  "white": "WhiteRunningLight",
  "off": "OffAlgo"
}

responses = {
  "no_such_algo": "Такого алгоритма не бывает",
  "too_slow": "Слишком медленно - смотри, замерзнешь!",
  "too_fast": "Слишком быстро - никто не догонит!",
  "faster": "Поехали быстрее!",
  "slower": "Тормозиии-и-и-и!!!",
  "changed_algo": "Поменяли алгоритм"
}

@app.route("/")
@app.route("/result/<result_name>")
def main(result_name = None):
  logging.info("Result name: %s", result_name)
  if result_name == None:
    return render_template("main.html")
  else:
    return render_template("main.html", last_command=responses[result_name])

@app.route("/algo/<algo_name>")
def algo(algo_name):
  if algo_name not in algos:
    logging.error("No such algorithm %s", algo_name)
    return redirect("/result/no_such_algo")
  else:
    logging.info("Requesting algo %s", algo_name)
    control_queue.put(ControlMessage(
      ControlMessage.MessageType.CHANGE_ALGO,
      algos[algo_name]))
  return redirect("/result/changed_algo")

@app.route("/speed/<direction>")
def speed(direction):
  if direction == "faster":
    if delay.faster():
      control_queue.put(ControlMessage(
        ControlMessage.MessageType.CHANGE_DELAY,
        delay.delay()))

      return redirect("/result/faster")
    else:
      return redirect("/result/too_fast")
  elif direction == "slower":
    if delay.slower():
      control_queue.put(ControlMessage(
        ControlMessage.MessageType.CHANGE_DELAY,
        delay.delay()))

      return redirect("/result/slower")
    else:
      return redirect("/result/too_slow")
  else:
    logging.info("Wrong direction: %s", direction)
    return redirect("/result/bad_speed")

class WebControlThread(threading.Thread):
  def __init__(self, q: queue.Queue, initial_delay: int):
    global control_queue, delay
    control_queue = q
    delay = SpeedControl(initial_delay)
    super().__init__()

  def run(self):
    app.run(host='0.0.0.0')


