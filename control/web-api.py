# This code is not currently being used.

import logging
import os
import queue
import threading

from control.message import ControlMessage

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')

from flask import Flask, render_template, redirect, jsonify

from algo import algos

MIN_SPEED = 0
MAX_SPEED = 100

app = Flask(__name__)
ALL_ALGOS = [x.__name__ for x in algos.GetAlgos()]
current_algo = ALL_ALGOS[0]
_current_speed = 50

@app.route("/algos", methods=["GET"])
def all_algos():
  return jsonify([
    {
      'algo': x,
      'is_current': x == current_algo,
      'algo_name': x # TODO: switch to x.GetName()
    }
  for x in ALL_ALGOS] )

@app.route("/set_algo/<algo>", methods=["GET", "POST"])
def set_algo(algo):
  if not algo in ALL_ALGOS:
    logging.error("Bad algo %s", algo)
    return f"No such algorithm {algo}", 400
  else:
    current_algo = algo
    logging.info("Current algorithm is now %s", current_algo)
    return ('', 204)

@app.route('/speed', methods=['GET'])
def get_speed():
  return jsonify(min_speed=MIN_SPEED, max_speed=MAX_SPEED, current_speed=_current_speed)

@app.route('/speed/<int:new_speed>', methods=['POST'])
def set_speed(new_speed):
  if not MIN_SPEED <= new_speed <= MAX_SPEED:
    return (f"Bad speed {new_speed}", 400)
  else:
    _current_speed = new_speed
    logging.info("New speed is %d", new_speed)
    return ('', 204)


class WebControlThread(threading.Thread):
  def __init__(self, q: queue.Queue, initial_delay: int):
    global control_queue, delay
    control_queue = q
    super().__init__()

  def run(self):
    app.run(host='0.0.0.0')


app.run(host='0.0.0.0')
