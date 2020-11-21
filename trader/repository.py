import json
import requests


class Repository:
    PUBLIC_API_BASE_PATH = "https://public-api.lykke.com/api"
    BASE_PATH_HFT_API = "https://hft-api.lykke.com/api"
    # 5years
    how_long_back_in_time_days = 1825

    def __init__(self, api_key, known_assets_ids):

        self.api_key = api_key

        # XRPCHF    XRP/CHF
        # LKK2YCHF  LKK2/CHF
        # EURCHF    EUR/CHF
        # ETHCHF    ETH/CHF
        # LKKCHF    LKK/CHF
        self.known_assets_ids = known_assets_ids

    def asset_pairs(self):
        print('Assets pairs \n')
        r = requests.get(Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/rate')
        list = r.json()
        for k in list:
            if k["id"] in (self.known_assets_ids):
                print('id: {0} bid: {1} ask: {2}'.format(k["id"], k["bid"], k["ask"]), end="\n")
        return list

    def assetPairsId(self, id):
        r = self.http.request('GET', Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/' + str(id))
        liste = json.loads(r.data)
        print(liste["Name"])
        return liste

    def isAlive(self):
        r = self.http.request('GET', Repository.PUBLIC_API_BASE_PATH + '/IsAlive')
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

        r = requests.post(url=Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/rate/history/' + asset_id,
                          data=json_body,
                          headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            print("Request failed with " + str(r.status_code) + ". Response body: " + str(r.json()))

        return r.json()

    def getBalance(self, assetId):
        r = requests.get(Repository.BASE_PATH_HFT_API + '/Wallets', headers={'api-key': self.api_key})
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
                              fields={'order': order, 'api-key': self.api_key})
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
                              fields={'order': order, 'api-key': self.api_key})
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
                              fields={'id': id, 'api-key': self.api_key})
        if r.status == 20:
            print("Order", id, "canceled")
            return True
        else:
            print("Order not canceled")
            return False

    def infoOrder(self, id):  # untested coz no api key given
        r = self.http.request('GET', 'https://hft-service-dev.lykkex.net/api/Orders/' + str(id),
                              fields={'id': id, 'api-key': self.api_key})
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
                                  fields={'api-key': self.api_key})
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
            if k["assetPair"] in (self.known_assets_ids):
                print('assetPair: {0} bid: {1} ask: {2} lastPrice: {3}'.format(k["assetPair"], k["bid"], k["ask"],
                                                                               k["lastPrice"]), end="\n")
        return liste
        print(liste)
