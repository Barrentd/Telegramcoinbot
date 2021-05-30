import re
import requests

url_coins ="https://api.coingecko.com/api/v3/coins/list"
url_currency ="https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
url_price="https://api.coingecko.com/api/v3/simple/price?"

resp_coins = requests.get(url_coins).json()
resp_currency = requests.get(url_currency).json()

def resp_mess(message):
  params = getcoininfo(message)
  req = requests.get(url=url_price, params=params).json()
  resp = displaycoin(req)
  return resp

def getcoininfo(id_coin):
  params = dict(
      ids=id_coin,
      vs_currencies='eur,usd',
      include_24hr_change='true',
  )
  return params

def displaycoin(respjson):
  res= next(iter(respjson))
  if not respjson[res]:
    answer = res.title()+" is empty"
  else:
    if next(iter(respjson[res])) == 'eur':
      coin = dict(
        name= res.title(),
        currency=respjson[res]['eur'],
        us_currency=respjson[res]['usd'],
        variation=respjson[res]['eur_24h_change'],
      )
      answer = strcoin(coin)
    else:
      symbol = dict(
        name= res.title(),
        symbol=respjson[res]['symbol'],
        rlname=respjson[res]['name'],
      )
      answer = strsymbol(symbol)
  return answer

def strcoin(coin):
  strname = 'Nom: '+coin['name']+'\n'
  strcurrency = 'Valeur: '+str(coin['currency'])+' Euros - '+str(coin['us_currency'])+' Dollars\n'
  if coin['variation'] != None:
    strvariation = 'Variation: '+str(round(coin['variation'],2))+' %'
  else:
    strvariation = 'Variation: '+str(coin['variation'])
  return strname + strcurrency + strvariation

def strsymbol(symbol):
  strname = 'Nom: '+symbol['name']+'\n'
  strsymbol = 'Symbol: '+symbol['symbol']+'\n'
  strrlname = 'Variation: '+symbol['rlname']
  return strname + strsymbol + strrlname
    
def matchcoin(mess_coin):
  res = None
  coinmatch = []
  for coin in resp_coins:
    if mess_coin == coin['id']:
      res = mess_coin
  if res == None:
    for coin in resp_coins:
      if re.search(mess_coin, coin['id']):
        coinmatch.append(coin['id'])
  return res, coinmatch