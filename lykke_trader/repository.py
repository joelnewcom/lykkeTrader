import json
import requests


class Repository:
    PUBLIC_API_BASE_PATH = "https://public-api.lykke.com/api"
    BASE_PATH_HFT_API = "https://hft-api.lykke.com/api"
    # 5years
    how_long_back_in_time_days = 1825

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def get_all_asset_pairs_rate():
        r = requests.get(Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/rate')
        return r.json()

    @staticmethod
    def get_asset_pairs_rate(asset_pair_id):
        r = requests.get(Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/rate/' + str(asset_pair_id))
        return r.json()

    @staticmethod
    def get_dictionary_asset_pairs_spot():
        r = requests.get(Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/dictionary/Spot')
        return r.json()

    @staticmethod
    def asset_pairs_id(id):
        r = requests.get(Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/' + str(id))
        asset_pairs = r.json()
        print(asset_pairs["Name"])
        return asset_pairs

    @staticmethod
    def is_alive():
        is_alive_response = requests.get(Repository.PUBLIC_API_BASE_PATH + '/IsAlive')
        if is_alive_response.status_code == 200:
            print("Server is alive, version :", is_alive_response.json()["version"])
            return True
        return False

    @staticmethod
    def get_history_rate(asset_id, date_time, period):
        json_body = json.dumps({"period": period, "dateTime": date_time})

        for x in range(5):
            try:
                r = requests.post(url=Repository.PUBLIC_API_BASE_PATH + '/AssetPairs/rate/history/' + asset_id,
                                  data=json_body,
                                  headers={'Content-Type': 'application/json'})
                if r.status_code == 200:
                    return r.json()
                else:
                    print("Request [URL: " + str(r.request.url) + "], [Body: " + str(
                        r.request.body) + "] failed with status code: " + str(r.status_code))
            except requests.exceptions.ConnectionError as exception:
                print('ConnectionException occurred: ' + exception)

    def get_balance(self, asset_id):
        r = requests.get(url=Repository.BASE_PATH_HFT_API + '/Wallets',
                         headers={'api-key': self.api_key})
        for k in r.json():
            print(k["Balance"], "of", k["AssetId"], "including", k["Reserved"], "reserved")
            if k["AssetId"] == asset_id:
                return k["Balance"] - k["Reserved"]
        raise Exception("Sorry, no numbers below zero")

    def marketOrder(self, assetId, buyorsell, volume):
        order = {"AssetPairId": assetId, "OrderAction": buyorsell, "Volume": volume}
        order = json.dumps(order)
        r = requests.post(Repository.BASE_PATH_HFT_API + '/Orders/market',
                          fields={'order': order, 'api-key': self.api_key})
        try:
            liste = r.json()
            try:
                print(liste["Error"])
                return False
            except:
                print("Executed market order", str(buyorsell), "volume :", volume, "on asset", str(assetId))
                return True
        except:
            return

    def limit_order_sell(self, asset_id, volume):
        order = {"AssetPairId": asset_id, "OrderAction": "sell", "Volume": volume}
        order = json.dumps(order)
        r = requests.post(Repository.BASE_PATH_HFT_API + '/Orders/limit',
                          fields={'order': order, 'api-key': self.api_key})
        try:
            response = r.json()
            try:
                print(response["Error"])
                return False
            except:
                print("Executed limit order", "sell", "volume :", volume, "on asset", str(asset_id))
                return True
        except:
            return  # print("Something went wrong :/")

    def limit_order_buy(self, asset_id, volume, price):
        order = {"AssetPairId": asset_id, "OrderAction": "Buy", "Volume": round(volume, 6), "Price": round(price, 6)}
        order = json.dumps(order)
        r = requests.post(Repository.BASE_PATH_HFT_API + '/Orders/v2/limit',
                          data=order,
                          headers={'api-key': self.api_key, 'Content-Type': 'application/json'})
        try:
            response = r.json()
            print(response)
            try:
                print(response["Error"])
                return False
            except:
                print("Executed limit order", "buy", "volume :", volume, "on asset", str(asset_id))
                return True
        except:
            print("Something went wrong :/")
            return

    def cancelOrder(self, id):  # untested coz no api key given
        r = requests.post('https://hft-service-dev.lykkex.net/api/Orders/' + str(id) + '/Cancel',
                          fields={'id': id, 'api-key': self.api_key})
        if r.status == 20:
            print("Order", id, "canceled")
            return True
        else:
            print("Order not canceled")
            return False

    def info_order(self, id):  # untested coz no api key given
        r = requests.get(Repository.BASE_PATH_HFT_API + '/Orders/' + str(id),
                         fields={'id': id, 'api-key': self.api_key})
        liste = r.json()
        print("Status", liste["Status"])
        print("Remaining volume", liste["RemainingVolume"])
        print("Price", liste["Price"], "on assets id", liste["AssetPairId"])
        return liste

    def allOrder(self):  # untested coz no api key given
        status = ["Pending", "InOrderBook", "Processing", "Matched", "NotEnoughFunds", "NoLiquidity", "UnknownAsset",
                  "Cancelled", "LeadToNegativeSpread"]
        for s in status:
            r = requests.get(Repository.BASE_PATH_HFT_API + '/Orders?status=' + s,
                             fields={'api-key': self.api_key})
            liste = r.json()
            print("Order", s)
            for k in liste:
                print("Remaining volume", k["RemainingVolume"])
                print("Price", k["Price"], "on assets id", k["AssetPairId"])
            print("")

    @staticmethod
    def order_book_asset(id):
        r = requests.get(Repository.BASE_PATH_HFT_API + '/OrderBooks/' + str(id))
        bid = []
        ask = []
        for k in r.json():
            if k["IsBuy"]:
                bid.extend(k["Prices"])  # bid
            else:
                ask.extend(k["Prices"])  # ask
        return bid, ask

    def get_market(self, known_assets_ids):
        print('Market data \n')
        r = requests.get('https://public-api.lykke.com/api/Market')
        liste = r.json()
        for k in liste:
            if k["assetPair"] in known_assets_ids:
                print('assetPair: {0} bid: {1} ask: {2} lastPrice: {3}'.format(k["assetPair"], k["bid"], k["ask"],
                                                                               k["lastPrice"]), end="\n")
        return liste
        print(liste)

    @staticmethod
    def get_history_trades(self, asset_pair_id):
        history_trades = requests.get(url=Repository.BASE_PATH_HFT_API + '/History/trades',
                                      fields={'api-key': self.api_key, 'assetPairId': asset_pair_id})
        return history_trades.json()
