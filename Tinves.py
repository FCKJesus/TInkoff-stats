import tinvest
import json
from datetime import datetime
from pytz import timezone


class InvesAccount:
	def __init__(self, key):	
		self.client = tinvest.SyncClient(key)
		self.moscow_tz = timezone('Europe/Moscow')
		self.FROM = self.moscow_tz.localize(datetime(2010, 1, 1, 0, 0))
		self.NOW = self.moscow_tz.localize(datetime.now())


	def get_market_stocks(self) -> dict:#словаь со всеми figi у брокера
		stocks = self.client.get_market_stocks().json()
		stocks = json.loads(stocks)['payload']['instruments']
		self.NAME = {}
		self.STOCKS = {}
		for stock in stocks:
			figi = stock['figi']
			currency = stock['currency']
			name = stock['name']
			ticker = stock['ticker']
			self.STOCKS[ticker] = figi
			self.NAME[ticker] = name
		return self.STOCKS, self.NAME



	def get_trades_sum(self, ticker, broker_account_id=None):#Считает прибыль/убыток по всем совершенным сделкам по одной акции
		ticker = "".join(c for c in ticker if c.isalpha()).upper()
		try:
			figi = self.STOCKS[ticker]
			name = self.NAME[ticker]
			operations = self.client.get_operations(from_=self.FROM, to=self.NOW, figi=figi, broker_account_id=broker_account_id).json()
			trades = json.loads(operations)['payload']['operations']
			if trades:
				payment_usd = 0
				payment_rub = 0
				payment_eur = 0
				for trade in trades:
					if trade['currency'] == 'USD':
						payment_usd += trade['payment']
					if trade['currency'] == 'RUB':
						payment_rub += trade['payment']
					if trade['currency'] == 'EUR':
						payment_eur += trade['payment']
				if ticker in self.figi_balance:
					if payment_usd != 0:
						return (name, payment_usd + self.ticker_balance[ticker],'USD')
					if payment_rub != 0:
						return (name, payment_rub + self.ticker_balance[ticker],'RUB')
					if payment_eur != 0:
						return (name, payment_eur + self.ticker_balance[ticker],'EUR')
				else:
					if payment_usd != 0:
						return (name, payment_usd,'USD')
					if payment_rub != 0:
						return (name, payment_rub,'RUB')
					if payment_eur != 0:
						return (name, payment_eur,'EUR')
			else:
				return 'Сделки не найдены'
		except KeyError:
			return 'Неизвестный тикер'
				

	def get_portfolio(self, broker_account_id=None):#Портфель
		positions = self.client.get_portfolio(broker_account_id=broker_account_id).json()
		currencies = self.client.get_portfolio_currencies(broker_account_id=broker_account_id).json()
		balance = json.loads(currencies)['payload']['currencies']
		stocks = json.loads(positions)['payload']['positions']
		self.RUB = balance[0]['balance']
		self.ticker_balance = {}
		self.figi_balance = {}
		for stock in stocks:
			self.figi_balance[stock['ticker']] = stock['figi']
			self.ticker_balance[stock['ticker']] = stock['average_position_price']['value'] * stock['balance'] + stock['expected_yield']['value']
		return self.figi_balance, self.ticker_balance
