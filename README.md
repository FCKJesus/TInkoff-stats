# Аналитика доходности сделок в Тинькофф брокере
###### Данный скрипт позволяет смотреть доходность по определеной акции, достаточно ввести ее тикер
Потребуются 2 библиотеки:
```
pip install tinvest
pip install pytz
```
Быстрый старт:
broker_account_id -  опционально, если есть несколько счетов
```
tinkoff = InvesAccount(key)
tinkoff.get_market_stocks()
tinkoff.get_portfolio(broker_account_id)
tinkoff.get_trades_sum(ticker, broker_account_id)
```
