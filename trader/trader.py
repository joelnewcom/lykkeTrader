import datetime
import json
import time
from datetime import datetime

import dateutil.relativedelta
import matplotlib.pyplot as plt
import datetime
import numpy as np
import requests


class trader:
    PUBLIC_API_BASE_PATH = "https://public-api.lykke.com/api"
    BASE_PATH_HFT_API = "https://hft-api.lykke.com/api"

    def __init__(self, apiKey, knownAssetsIds):

        self.APIKEY = apiKey

        # XRPCHF    XRP/CHF
        # LKK2YCHF  LKK2/CHF
        # EURCHF    EUR/CHF
        # ETHCHF    ETH/CHF
        # LKKCHF    LKK/CHF
        self.KNOWN_ASSETS_IDS = knownAssetsIds

    def assetPairs(self):
        print('Assetsparis \n')
        r = requests.get(trader.PUBLIC_API_BASE_PATH + '/AssetPairs/rate')
        liste = r.json()
        for k in liste:
            if k["id"] in (self.KNOWN_ASSETS_IDS):
                print('id: {0} bid: {1} ask: {2}'.format(k["id"], k["bid"], k["ask"]), end="\n")
        return liste

    def assetPairsId(self, id):
        r = self.http.request('GET', trader.PUBLIC_API_BASE_PATH + '/AssetPairs/' + str(id))
        liste = json.loads(r.data)
        print(liste["Name"])
        return liste

    def isAlive(self):
        r = self.http.request('GET', trader.PUBLIC_API_BASE_PATH + '/IsAlive')
        liste = json.loads(r.data)
        try:
            print("Server is alive, version :", liste["Version"])
            if liste["IssueIndicators"] != []:
                print("Issues indicators :")
                for k in liste["IssueIndicators"]:
                    print(k)
            else:
                print("Without issue indicators x)")
            return True
        except:
            print("Server is dead, due to :", liste["ErrorMessage"])
            return False

    def get_history(self, asset_id, date_time):
        json_body = json.dumps({"period": "Month", "dateTime": date_time})

        r = requests.post(url=trader.PUBLIC_API_BASE_PATH + '/AssetPairs/rate/history/' + asset_id,
                          data=json_body,
                          headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            print("Request failed with " + str(r.status_code) + ". Response body: " + str(r.json()))

        return r.json()

    def getBalance(self, assetId):
        r = requests.get(trader.BASE_PATH_HFT_API + '/Wallets', headers={'api-key': self.APIKEY})
        liste = r.json()
        for k in liste:
            print(k["Balance"], "of", k["AssetId"], "including", k["Reserved"], "reserved")
            if k["AssetId"] == assetId:
                return k["Balance"] - k["Reserved"]
        raise Exception("Sorry, no numbers below zero")

    def marketOrder(self, assetId, buyorsell, volume):
        order = {"AssetPairId": assetId, "OrderAction": buyorsell, "Volume": volume}
        order = json.dumps(order)
        r = self.http.request('POST', 'https://hft-service-dev.lykkex.net/api/Orders/market',
                              fields={'order': order, 'api-key': self.APIKEY})
        try:
            liste = json.loads(r.data)
            try:
                print(liste["Error"])
                return False
            except:
                print("Executed market order", str(buyorsell), "volume :", volume, "on asset", str(assetId))
                return True
        except:
            return

    def limitOrder(self, assetId, buyorsell, volume):
        order = {"AssetPairId": assetId, "OrderAction": buyorsell, "Volume": volume}
        order = json.dumps(order)
        r = self.http.request('POST', 'https://hft-service-dev.lykkex.net/api/Orders/limit',
                              fields={'order': order, 'api-key': self.APIKEY})
        try:
            liste = json.loads(r.data)
            try:
                print(liste["Error"])
                return False
            except:
                print("Executed limit order", str(buyorsell), "volume :", volume, "on asset", str(assetId))
                return True
        except:
            return  # print("Something went wrong :/")

    def cancelOrder(self, id):  # untested coz no api key given
        r = self.http.request('POST', 'https://hft-service-dev.lykkex.net/api/Orders/' + str(id) + '/Cancel',
                              fields={'id': id, 'api-key': self.APIKEY})
        if r.status == 20:
            print("Order", id, "canceled")
            return True
        else:
            print("Order not canceled")
            return False

    def infoOrder(self, id):  # untested coz no api key given
        r = self.http.request('GET', 'https://hft-service-dev.lykkex.net/api/Orders/' + str(id),
                              fields={'id': id, 'api-key': self.APIKEY})
        liste = json.loads(r.data)
        print("Status", liste["Status"])
        print("Remaining volume", liste["RemainingVolume"])
        print("Price", liste["Price"], "on assets id", liste["AssetPairId"])
        return liste

    def allOrder(self):  # untested coz no api key given
        status = ["Pending", "InOrderBook", "Processing", "Matched", "NotEnoughFunds", "NoLiquidity", "UnknownAsset",
                  "Cancelled", "LeadToNegativeSpread"]
        for s in status:
            r = self.http.request('GET', 'https://hft-service-dev.lykkex.net/api/Orders?status=' + s,
                                  fields={'api-key': self.APIKEY})
            liste = json.loads(r.data)
            print("Order", s)
            for k in liste:
                print("Remaining volume", k["RemainingVolume"])
                print("Price", k["Price"], "on assets id", k["AssetPairId"])
            print("")

    def orderBookAssetself(self, id):
        r = self.http.request('GET', 'https://hft-service-dev.lykkex.net/api/OrderBooks/' + str(id))
        # isBuy looks like useless coz false => negative value of volume
        liste = json.loads(r.data)
        buy = []
        sell = []
        for k in liste:
            if k["IsBuy"]:
                buy.extend(k["Prices"])
            else:
                sell.extend(k["Prices"])
        return (buy, sell)

    def getMarket(self):
        print('Market data \n')
        r = self.http.request('GET', 'https://public-api.lykke.com/api/Market')
        liste = json.loads(r.data)
        for k in liste:
            if k["assetPair"] in (self.KNOWN_ASSETS_IDS):
                print('assetPair: {0} bid: {1} ask: {2} lastPrice: {3}'.format(k["assetPair"], k["bid"], k["ask"],
                                                                               k["lastPrice"]), end="\n")
        return liste
        print(liste)

    def run(self):
        # Buy low sell high, low level => we don't look at volume
        volumeTraded = 50
        assetTraded = "CHF"
        frequency = 0.5

        # End of parameters
        miniBuy = 99999999999
        maxiSell = 0
        notBuyYet = True
        notSellYet = True

        moneyToSpend = self.getBalance("CHF")
        print("money to spend: {0}".format(moneyToSpend))

        month_delta = dateutil.relativedelta.relativedelta(months=1)
        date = datetime.datetime.now()

        x = np.empty(0)
        y = np.empty(0)

        for i in range(14):
            date_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
            print("requested date: " + str(date_time))
            history = self.get_history("ETHCHF", date_time)
            x = np.append(x, date)
            y = np.append(y, history["ask"])
            print("aks price: " + str(history["ask"]))
            date = date - month_delta
            time.sleep(11)

        plt.plot(x, y)
        plt.show()

        # getMarket()
        # assetPairs()

        # while True:
        #     time.sleep(1 / frequency)
        #     # First we uptade miniBuy and maxiSell
        #     buy, sell = orderBookAsset(assetTraded)
        #     buyAvalable = min([i["Price"] for i in buy])
        #     sellAvalable = max([i["Price"] for i in sell])
        #
        #     miniBuy = min(miniBuy, buyAvalable)
        #     maxiSell = max(maxiSell, sellAvalable)
        #     print("Order book analysed // min buy :", miniBuy, " // top sell :", maxiSell, "// spread :", maxiSell - miniBuy)
        #
        #     # We then look if we can buy lower than maxiSell or sell higher than maxiBuy
        #     if buyAvalable < maxiSell and notBuyYet:
        #         notBuyYet = not marketOrder(assetTraded, "Buy", volumeTraded)
        #     if sellAvalable > miniBuy and notSellYet:
        #         notSellYet = not marketOrder(assetTraded, "Sell", volumeTraded)
        #
        #     # End of the strategy, we may loop on assets using multithreading, was asking simple strategy : it cant lose
