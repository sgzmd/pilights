import enum
import logging
import queue
import threading

import prompt
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from algo import LightsAlgo


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


class ConsoleControlThread(threading.Thread):
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


class TelegramControlThread(threading.Thread):
  _dispatcher: telegram.ext.Dispatcher = None

  def __init__(self, q: queue.Queue, token: str):
    self._q = q
    self._updater = Updater(token, use_context=True)
    self._dispatcher = self._updater.dispatcher
    super().__init__()

  def main_menu_keyboard(self):
    keyboard = [[InlineKeyboardButton('Выбрать алгоритм', callback_data='algo')],
                [InlineKeyboardButton('Выбрать скорость', callback_data='speed')],
                [InlineKeyboardButton('Узнать больше', callback_data='info')]]
    return InlineKeyboardMarkup(keyboard)

  def algo_menu_handler(self, update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Выберите новый алгоритм", reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('Звездная ночь', callback_data='new_algo_starrynight')],
      [InlineKeyboardButton('Радуга', callback_data='newalgo_rainbow')],
    ]))

  def starry_night(self, update: Update, context: CallbackContext):
    self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_ALGO,
          "StarryNight"))
    update.callback_query.message.reply_text("А пожалуйста!")

  def rainbow(self, update: Update, context: CallbackContext):
    self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_ALGO,
          "RotateAndLuminance"))
    update.callback_query.message.reply_text("Легко!")


  def hello(self, update: Update, context: CallbackContext):
    logging.info("Received update: %s", update)
    update.message.reply_text("Добро пожаловать! Чего изволите?", reply_markup=self.main_menu_keyboard())

  def algo(self, update: Update, context: CallbackContext):
    logging.info("Received update: %s", update)

  def run(self):
    self._dispatcher.add_handler(CommandHandler("start", self.hello))
    self._dispatcher.add_handler(CallbackQueryHandler(self.starry_night, "^newalgo_starrynight"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.rainbow, "^newalgo_rainbow"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.algo_menu_handler, "^algo"))
    self._updater.start_polling()
