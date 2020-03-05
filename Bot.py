import os
import logging
import time
import sys

from collections import deque

import OrderBook as ob

log = logging.getLogger('main')
logF = logging.getLogger('main_file')
logAllMessage = logging.getLogger('log_file_info')

class Bot():
	def __init__(self, EUR = 0.0, ETC = 0.0, percent_gain = 0.0, percent_loss = 0.0, deque_max_len = 3):

		self._EUR = EUR
		self._ETC = ETC

		self._order_price = 0
		self._previous_price = deque([], deque_max_len)
		print("str len deque: " + str(len(self._previous_price)))

		# Need to update in function of taker / maker fee
		self._percent_gain = percent_gain
		self._percent_loss = percent_loss

		self._fee_from_buy = 0

		self.Order_Book = ob.OrderBook(callback_array = {'ticker':self.callback_ticker, 'l2update':self.callback_update})
		
		self.fileOrderBook = open("OrderBook.txt","w")
		self.go()


	def go(self):
		self.fileOrderBook.write(str(self.Order_Book))
		self.Order_Book.start()
		try:
			while True:
				time.sleep(10)
				self.fileOrderBook.write(str(self.Order_Book))
		except KeyboardInterrupt:
			self.Order_Book.close()

		self.fileOrderBook.close()
		if self.Order_Book.error:
			sys.exit(1)
		else:
			sys.exit(0)

	
	def callback_ticker(self, current_price):
		print('-----> Bot: ticker message // order_price: ' + str(self._order_price) + ' // current_price: ' + str(current_price))
		
		current_change = 0
		change_order_price = 0

		# Temporary, need to be deleted when order_price will be correctly set
		if self._order_price == 0:
			self._order_price = float(current_price)
			self.buyAll(current_price)

		if self._order_price != 0:
			change_order_price = round(((current_price - self._order_price) / self._order_price) * 100, 4)
			print("Change Order Price: " + str(change_order_price))
			logF.debug("-----> Change Order Price: " + str(change_order_price))

		if len(self._previous_price) != 0 and self._previous_price[0] != 0:
			current_change = round(((current_price - self._previous_price[0]) / self._previous_price[0]) * 100, 4)
			print("Current price: " + str(current_price) + " // Previous Price: " + str(self._previous_price[0]) + " // Change(%):" + str(current_change))

		self._previous_price.appendleft(current_price)
		print(self._previous_price)

		if (change_order_price > 1.4) and (current_change < 0.0): # Sell
			self.sellAll(current_price)
		elif change_order_price < -1.5: # Stop loss
			self.sellAll(current_price)
		elif (change_order_price < -0.7) or (current_change > 0.0 and change_order_price > 0 and self._ETC == 0): # Buy
			self.buyAll(current_price)
		# Else
			# Nothing To Do
		

	def callback_update(self):
		# print('-----> Bot: L2update message')
		# Do nothing
		return


	def sellAll(self, current_price):
		if self._ETC != 0:
			self._EUR = (self._ETC * current_price) - (self._ETC * current_price * 0.005)

			self._ETC = 0
			self._fee_from_buy = 0
			self._order_price = current_price

			log.debug('SellAll - Current EUR: ' + str(self._EUR) + ' // Current ETC: ' + str(self._ETC))

		logF.debug('SellAll - Current EUR: ' + str(self._EUR) + ' // Current ETC: ' + str(self._ETC))


	def buyAll(self, current_price):
		if self._EUR != 0:
			self._ETC = (self._EUR / current_price) - ((self._EUR / current_price) * 0.005)

			self._fee_from_buy = self._EUR * 0.005

			self._EUR = 0
			self._order_price = current_price

			log.debug('BuyAll - Current EUR: ' + str(self._EUR) + ' // Current ETC: ' + str(self._ETC))

		logF.debug('BuyAll - Current EUR: ' + str(self._EUR) + ' // Current ETC: ' + str(self._ETC))
