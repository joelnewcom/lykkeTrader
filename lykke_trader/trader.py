import json
import time
from datetime import datetime
import dateutil.relativedelta
import matplotlib.pyplot as plt
import datetime
import numpy as np


class Trader:


    def __init__(self, repository, known_assets_ids):

        self.repository = repository
        self.known_assets_ids = known_assets_ids

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

        moneyToSpend = self.repository.getBalance("CHF")
        print("money to spend: {0}".format(moneyToSpend))

        month_delta = dateutil.relativedelta.relativedelta(months=1)
        date = datetime.datetime.now()

        x = np.empty(0)
        y = np.empty(0)

        for i in range(3):
            date_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
            print("requested date: " + str(date_time))
            history = self.repository.get_history("ETHCHF", date_time)
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
