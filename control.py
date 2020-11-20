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

  DELAY_STEP = 100

  def __init__(self, q: queue.Queue, token: str, delay: int):
    self._q = q
    self._delay = delay
    self._updater = Updater(token, use_context=True)
    self._dispatcher = self._updater.dispatcher
    super().__init__()

  def check_username(self, update: Update):
    if not update.effective_user.username in ["sgzmd"]:
      logging.error("Access denied for user %s", update.effective_user.username)
      update.message.reply_text("Not authorized")
      return False
    else:
      return True

  def main_menu_keyboard(self):
    keyboard = [[InlineKeyboardButton('Выбрать алгоритм', callback_data='algo')],
                [InlineKeyboardButton('Выбрать скорость', callback_data='speed')],
                [InlineKeyboardButton('Узнать больше', callback_data='info')]]
    return InlineKeyboardMarkup(keyboard)

  def algo_menu_handler(self, update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Выберите новый алгоритм", reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('Звездная ночь', callback_data='starrynight')],
      [InlineKeyboardButton('Радуга', callback_data='rainbow')],
    ]))

  def speed_menu_handler(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    update.callback_query.message.reply_text("Как надо?", reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('Быстрее!', callback_data='faster')],
      [InlineKeyboardButton('Медленнее...', callback_data='slower')],
    ]))

  def speed_slow(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    if self._delay >= 1000:
      update.callback_query.message.reply_text("Слишком медленно, дальше я усну!")
    else:
      self._delay += self.DELAY_STEP
      self._q.put_nowait(ControlMessage(
        ControlMessage.MessageType.CHANGE_DELAY,
        self._delay))
      update.callback_query.message.reply_text("Тормозии-и-и-и!!!", reply_markup=self.main_menu_keyboard())

  def speed_fast(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    if self._delay < 100:
      update.callback_query.message.reply_text("Слишком быстро - смотрии, не поймаешь!!")
    else:
      self._delay -= self.DELAY_STEP
      self._q.put_nowait(ControlMessage(
        ControlMessage.MessageType.CHANGE_DELAY,
        self._delay))
      update.callback_query.message.reply_text("Побежали!!", reply_markup=self.main_menu_keyboard())


  def starry_night(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_ALGO,
          "StarryNight"))
    update.callback_query.message.reply_text("А пожалуйста!", reply_markup=self.main_menu_keyboard())

  def rainbow(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    self._q.put_nowait(ControlMessage(
          ControlMessage.MessageType.CHANGE_ALGO,
          "RotateAndLuminance"))
    update.callback_query.message.reply_text("Легко!", reply_markup=self.main_menu_keyboard())


  def hello(self, update: Update, context: CallbackContext):
    if not self.check_username(update):
      return

    logging.info("Received update: %s", update)
    update.message.reply_text("Добро пожаловать! Чего изволите?", reply_markup=self.main_menu_keyboard())

  def algo(self, update: Update, context: CallbackContext):
    logging.info("Received update: %s", update)

  def run(self):
    self._dispatcher.add_handler(CommandHandler("start", self.hello))
    self._dispatcher.add_handler(CallbackQueryHandler(self.starry_night, pattern="starrynight"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.rainbow, pattern="rainbow"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.algo_menu_handler, pattern="algo"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.speed_menu_handler, pattern="speed"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.speed_fast, pattern="faster"))
    self._dispatcher.add_handler(CallbackQueryHandler(self.speed_slow, pattern="slower"))
    self._updater.start_polling()
