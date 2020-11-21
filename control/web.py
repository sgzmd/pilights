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

algos = {
  "starry_night": "StarryNight",
  "rainbow": "RotateAndLuminance",
  "white": "WhiteRunningLight"
}

@app.route("/")
def main():
  return render_template("main.html")

@app.route("/algo/<algo_name>")
def algo(algo_name):
  logging.info("Requesting algo %s", algo_name)
  if algo_name not in algos:
    logging.error("No such algorithm %s", algo_name)
    return redirect("/?no_such_algo")
  else:
    logging.info("Requesting algo %s", algo_name)
    control_queue.put_nowait(ControlMessage(
      ControlMessage.MessageType.CHANGE_ALGO,
      algos[algo_name]))
  return redirect("/")

class WebControlThread(threading.Thread):
  def __init__(self, q: queue.Queue):
    global control_queue
    control_queue = q
    super().__init__()

  def run(self):
    app.run()


