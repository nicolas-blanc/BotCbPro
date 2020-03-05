from sortedcontainers import SortedDict

import os

import cbpro

import logging

log = logging.getLogger('main')
logF = logging.getLogger('main_file')
logAllMessage = logging.getLogger('log_file_info')

class OrderBook(cbpro.WebsocketClient):
	def __init__(self, callback_array = None):
		super(OrderBook, self).__init__(url=os.getenv("API_URL_WS_FEED"), products=["ETC-EUR"], channels=["level2", "ticker"], api_key=os.getenv("API_KEY"), api_secret=os.getenv("API_SECRET"), api_passphrase=os.getenv("API_PASSPHRASE"))

		self.auth = cbpro.AuthenticatedClient(key=self.api_key, b64secret=self.api_secret, passphrase=self.api_passphrase, api_url=os.getenv("API_URL_REST_API"))

		self._buy = SortedDict()
		self._sell = SortedDict()

		self._current_price = 0.0

		self._low_24h_price = 0.0
		self._high_24h_price = 0.0

		self._callback_array = callback_array
		print("****** > " + str(callback_array))

		self.update_fees()


	def __str__(self):
		string_return = '--/\--/\--/\--/\--/\--/\--/\--/\--/\--/\--'

		string_return += '\n * Products: '
		for product in self.products:
			string_return += product + ' / '

		string_return += '\n * Channels: '
		for channel in self.channels:
			string_return += channel + ' / '

		string_return += '\n * Current Price: ' + str(self._current_price)
		string_return += '\n * Low 24h Price: ' + str(self._low_24h_price)
		string_return += '\n * High 24h Price: ' + str(self._high_24h_price)

		# string_return += '\n * Fees - Maker: ' + str(self._current_fees_maker) + ' / Taker: ' + str(self._current_fees_taker)

		# string_return += '\n * Percent gain: ' + str(self._percent_gain) + ' / Percent loss: ' + str(self._percent_loss)

		number_of_item = 5
		string_return += '\n * Buy Order Book:'
		len_buy = len(self._buy)
		rng = len_buy - number_of_item
		if rng < 0:
			rng = 0
		for i in range(rng, len_buy):
			(key, value) = self._buy.peekitem(i)
			string_return += '\n	- Price: ' + str(key) + ', Size: ' + str(value)

		string_return += '\n * Sell Order Book:'
		rng = number_of_item
		if len(self._sell) < rng:
			rng = len(self._sell) - 1
		for i in range(0, rng):
			(key, value) = self._sell.peekitem(i)
			string_return += '\n	- Price: ' + str(key) + ', Size: ' + str(value)

		string_return += '\n--\/--\/--\/--\/--\/--\/--\/--\/--\/--\/--\n'
		return string_return


	def on_message(self, message):
		# super(OrderBook, self).on_message(message)
		logAllMessage.info(" *** " + str(message) + " *** ")

		msg_type = message['type']
		if msg_type == 'snapshot':
			log.debug('-----> Snapshot message')
			self.init_order_book(message)
		elif msg_type == 'l2update':
			# log.debug('-----> L2update message')
			self.change_order_book(message)
			if self._callback_array['l2update'] != None:
				self._callback_array['l2update']()
			else:
				log.warning('----->No Callback: L2update message')
		elif msg_type == 'ticker':
			# log.debug('-----> ticker message')
			self.update_ticker(message)
			if self._callback_array['ticker'] != None:
				self._callback_array['ticker'](self._current_price)
			else:
				log.warning('----->No Callback: Ticker message')
		else:
			log.warning('This type * ' + str(msg_type) + ' * is not traited:\n --- ' + str(message) + ' ---')


	def on_open(self):
		super(OrderBook, self).on_open()


	def on_close(self):
		super(OrderBook, self).on_close()


	def update_fees(self):
		current_fees = self.auth._send_message('get', '/fees')
		self._current_fees_taker = float(current_fees['taker_fee_rate'])
		self._current_fees_maker = float(current_fees['maker_fee_rate'])


	def init_order_book(self, message):
		bids = message['bids']
		asks = message['asks']

		for bid in bids:
			# logF.debug(' - bid - ' + str(bid))
			self._buy[float(bid[0])] = float(bid[1])
		
		for ask in asks:
			# logF.debug(' - ask - ' + str(ask))
			self._sell[float(ask[0])] = float(ask[1])


	def change_order_book(self, message):
		changes = message['changes']

		for change in changes:
			if change[0] == 'buy':
				if change[2] == '0':
					del self._buy[float(change[1])]
				else:
					self._buy[float(change[1])] = float(change[2])
			elif change[0] == 'sell':
				if change[2] == '0':
					del self._sell[float(change[1])]
				else:
					self._sell[float(change[1])] = float(change[2])
			else:
				log.warning('Not a Buy or Sell changes: ' + str(change))

	def update_ticker(self, message):
		self._current_price = float(message['price'])

		self._low_24h_price = float(message['low_24h'])
		self._high_24h_price = float(message['high_24h'])