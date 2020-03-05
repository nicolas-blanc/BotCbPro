import time
import sys
import datetime as dt

import cbpro
from pymongo import MongoClient
#from itertools import islice

import logging

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter_2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter_3 = logging.Formatter('%(asctime)s - %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler('debug.log', mode='w+')
fh.setLevel(logging.DEBUG)

fh_2 = logging.FileHandler('LogAllMessage.log')
fh_2.setLevel(logging.INFO)

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter_2)
fh_2.setFormatter(formatter_3)

# add ch to logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger_file = logging.getLogger('main_file')
logger_file.setLevel(logging.DEBUG)
logger_file.addHandler(fh)

logger_file_2 = logging.getLogger('log_file_info')
logger_file_2.setLevel(logging.INFO)
logger_file_2.addHandler(fh_2)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

import AllTestInText as al
import Bot

print('Hello World!')

allTest = al.AllTestInText()
allTest.launch_all_test()

fileOrderBook = open("OrderBook.txt","w")

StartMoney = 200

bot = Bot.Bot(EUR = StartMoney)

# Order_Book = ob.OrderBook()
# Order_Book.start()

# fileOrderBook.write(str(Order_Book))

# try:
# 	while True:
# 		time.sleep(10)
# 		fileOrderBook.write(str(Order_Book))
# except KeyboardInterrupt:
# 	Order_Book.close()

# fileOrderBook.close()
# if Order_Book.error:
# 	sys.exit(1)
# else:
# 	sys.exit(0)

'''
# See to connect to a MongoDB after the implementation of the bot ?
# import PyMongo and connect to a local, running Mongo instance
mongo_client = MongoClient('mongodb://localhost:27017/')

# specify the database and collection
db = mongo_client.cryptocurrency_database
XRP_collection = db.XRP_collection

# instantiate a WebsocketClient instance, with a Mongo collection as a parameter
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="XRP-EUR", mongo_collection=XRP_collection, should_print=False, channels=["level2"])
wsClient.start()

try:
	while True:
		time.sleep(10)
except KeyboardInterrupt:
	wsClient.close()

if wsClient.error:
	sys.exit(1)
else:
	sys.exit(0)
#'''

'''
class OrderBookConsole(cbpro.OrderBook):
# Logs real-time changes to the bid-ask spread to the console

	def __init__(self, product_id=None, channels=None):
		super(OrderBookConsole, self).__init__(product_id=product_id)

		self.channels = channels
		# latest values of bid-ask spread
		self._bid = None
		self._ask = None
		self._bid_depth = None
		self._ask_depth = None

		self._fileOrderBook = None;

	def on_message(self, message):
		super(OrderBookConsole, self).on_message(message)
		# print("----->" + str(message) + '\n')
		self._fileOrderBook.write("\n ----> " + str(message))
		# Calculate newest bid-ask spread
		bid = self.get_bid()
		bids = self.get_bids(bid)
		bid_depth = sum([b['size'] for b in bids])
		ask = self.get_ask()
		asks = self.get_asks(ask)
		ask_depth = sum([a['size'] for a in asks])

		if self._bid == bid and self._ask == ask and self._bid_depth == bid_depth and self._ask_depth == ask_depth:
			# If there are no changes to the bid-ask spread since the last update, no need to print
			self._fileOrderBook.write("\n  ---  pass  ---")
			pass
		else:
			# If there are differences, update the cache
			self._bid = bid
			self._ask = ask
			self._bid_depth = bid_depth
			self._ask_depth = ask_depth
			mess = (' /.\\ {} {} bid: {:.3f} @ {:.2f}\task: {:.3f} @ {:.2f} /*\\ \n'.format(
			dt.datetime.now(), self.product_id, bid_depth, bid, ask_depth, ask))
			print(mess)
			self._fileOrderBook.write("\n" + str(mess))

	def on_open(self):
		super(OrderBookConsole, self).on_open()
		self._fileOrderBook = open("WebSocketOrderBook.txt","w")

	def on_close(self):
		super(OrderBookConsole, self).on_close()
		self._fileOrderBook.close()
		print(' *** Stop *** ')



order_book = OrderBookConsole(product_id="BTC-EUR" , channels=["level2"])
order_book.start()

try:
	while True:
		time.sleep(10)
except KeyboardInterrupt:
	order_book.close()

if order_book.error:
	sys.exit(1)
else:
	sys.exit(0)
#'''

print('Hello World WebSocket done')
