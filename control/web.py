import logging
import threading
import queue
import os

from control.message import ControlMessage

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')

from flask import Flask, render_template, redirect

templates = os.path.abspath(os.path.dirname(__file__) + "/../templates")
logging.info("Flask will be looking for templates in %s", templates)
app = Flask(__name__, template_folder=templates)

control_queue: queue.Queue = None
delay: int = None

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

algos = {
  "starry_night": "StarryNight",
  "rainbow": "RotateAndLuminance",
  "white": "WhiteRunningLight"
}

@app.route("/")
@app.route("/result/<result_name>")
def main(result_name = None):
  logging.info("Result name: %s", result_name)
  return render_template("main.html")

@app.route("/algo/<algo_name>")
def algo(algo_name):
  if algo_name not in algos:
    logging.error("No such algorithm %s", algo_name)
    return redirect("/result/no_such_algo")
  else:
    logging.info("Requesting algo %s", algo_name)
    control_queue.put_nowait(ControlMessage(
      ControlMessage.MessageType.CHANGE_ALGO,
      algos[algo_name]))
  return redirect("/result/changed_algo")

@app.route("/speed/<direction>")
def speed(direction):
  if direction == "faster":
    pass
  elif direction == "slower":
    pass
  else:
    logging.info("Wrong direction: %s", direction)
    return redirect("/result/bad_speed")

class WebControlThread(threading.Thread):
  def __init__(self, q: queue.Queue, initial_delay: int):
    global control_queue, delay
    control_queue = q
    delay = initial_delay
    super().__init__()

  def run(self):
    app.run()


