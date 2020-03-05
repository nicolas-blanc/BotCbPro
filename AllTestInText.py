import cbpro
import os

#API Secret Key = sFmQy9dxj1+i5OykxzB19VpHLI99ZubiDCDGKRJHlvSXrrn8yj+bnLpPpR1efZ7JB2PFfWfBAhg5t1jzlDrTuw==

class AllTestInText():
	def __init__(self):
		self.folder = "./log_cbpro/"

		self._public_client = cbpro.PublicClient()

		self._key = os.getenv("API_KEY_SANDBOX")
		self._b64secret = os.getenv("API_SECRET_SANDBOX")
		self._passphrase = os.getenv("API_PASSPHRASE_SANDBOX")

		self._auth_client = cbpro.AuthenticatedClient(self._key, self._b64secret, self._passphrase, api_url="https://api-public.sandbox.pro.coinbase.com")

	def launch_all_test(self):
		self.auth_buy_limit()
		self.auth_buy_market()
		self.auth_sell_limit()
		self.auth_sell_market()
		self.get_account()
		self.get_account_history()
		self.get_account_holds()
		self.get_accounts()
		self.get_currencies()
		self.get_product()
		self.get_product_24hr_stats()
		self.get_product_historic_rates()
		self.get_product_order_book()
		self.get_product_ticker()
		self.get_product_trades()
		self.get_time()

# ----- Public Client -----
	def get_product(self):
		file = open(self.folder + "get_products.txt","w")
		file.write(str(self._public_client.get_products()))
		file.close()

	def get_product_order_book(self):
		file = open(self.folder + "get_product_order_book.txt","w")
		file.write(str(self._public_client.get_product_order_book('XRP-EUR', level=3)))
		file.close()

	def get_product_ticker(self):
		file = open(self.folder + "get_product_ticker.txt","w")
		file.write(str(self._public_client.get_product_ticker(product_id='XRP-EUR')))
		file.close()

	def get_product_trades(self):
		historic_rates_gen = self._public_client.get_product_trades(product_id='XRP-EUR')
		file = open(self.folder + "get_product_trades.txt","w")
		file.write(str(list(historic_rates_gen)))
		file.close()

	def get_product_historic_rates(self):
		file = open(self.folder + "get_product_historic_rates.txt","w")
		file.write(str(self._public_client.get_product_historic_rates('XRP-EUR')))
		file.close()

	def get_product_24hr_stats(self):
		file = open(self.folder + "get_product_24hr_stats.txt","w")
		file.write(str(self._public_client.get_product_24hr_stats('XRP-EUR')))
		file.close()

	def get_currencies(self):
		file = open(self.folder + "get_currencies.txt","w")
		file.write(str(self._public_client.get_currencies()))
		file.close()

	def get_time(self):
		file = open(self.folder + "get_time.txt","w")
		file.write(str(self._public_client.get_time()))
		file.close()
# ----- ----- ------ -----

# ----- Authenticated Client -----
	def get_accounts(self):
		file = open(self.folder + "auth_get_accounts.txt","w")
		file.write(str(self._auth_client.get_accounts()))
		file.close()

	def get_account(self):
		file = open(self.folder + "auth_get_account.txt","w")
		file.write(str(self._auth_client.get_account("72f2c996-0b93-4bae-91d0-562eecef9914")))
		file.close()

	def get_account_history(self):
		file = open(self.folder + "auth_get_account_history.txt","w")
		file.write(str(self._auth_client.get_account_history("72f2c996-0b93-4bae-91d0-562eecef9914")))
		file.close()

	def get_account_holds(self):
		file = open(self.folder + "auth_get_account_holds.txt","w")
		file.write(str(self._auth_client.get_account_holds("72f2c996-0b93-4bae-91d0-562eecef9914")))
		file.close()

	def auth_buy_limit(self):
		file = open(self.folder + "auth_buy_limit.txt","w")
		file.write(str(self._auth_client.buy(price='100.00', size='0.01', order_type='limit', product_id='BTC-EUR')))
		file.close()

	def auth_buy_market(self):
		file = open(self.folder + "auth_buy_market.txt","w")
		file.write(str(self._auth_client.place_market_order(product_id='BTC-EUR', side='buy', funds='100.00')))
		file.close()

	def auth_sell_limit(self):
		file = open(self.folder + "auth_sell_limit.txt","w")
		file.write(str(self._auth_client.sell(price='100.00', size='0.01', order_type='limit', product_id='BTC-EUR')))
		file.close()
		
	def auth_sell_market(self):
		file = open(self.folder + "auth_sell_market.txt","w")
		file.write(str(self._auth_client.place_market_order(product_id='BTC-EUR', side='sell', funds='90.00')))
		file.close()
# ----- ----- ----- ----- -----
