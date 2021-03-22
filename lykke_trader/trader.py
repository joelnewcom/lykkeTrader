import json
import time
from datetime import datetime
import dateutil.relativedelta
import matplotlib.pyplot as plt
import datetime
import numpy as np


class Trader:

    def __init__(self, repository, known_assets_ids, librarian):

        self.repository = repository
        self.known_assets_ids = known_assets_ids
        self.librarian = librarian

    def run(self):
        volumeTraded = 50
        assetTraded = "CHF"
        frequency_in_seconds = 2


        money_to_spend = self.repository.get_balance("CHF")
        print("money to spend: {0}".format(money_to_spend))

        while True:
            time.sleep(frequency_in_seconds)

            bid, ask = self.repository.order_book_asset("XRPCHF")

            # Bid = Other people want to buy at this price
            # Ask = Other want to sell at this price

            # Sell to max buy, Buy at min ask

            highest_bid = max([i["Price"] for i in bid])
            lowest_ask = min([i["Price"] for i in ask])

            # spread = highest bid - lowest ask
            spread = highest_bid - lowest_ask


            # We then look if we can buy lower than maxiSell or sell higher than maxiBuy
            if buyAvalable < maxiSell and notBuyYet:
                notBuyYet = not self.repository.marketOrder(assetTraded, "Buy", volumeTraded)
            if sellAvalable > miniBuy and notSellYet:
                notSellYet = not self.repository.marketOrder(assetTraded, "Sell", volumeTraded)

            # End of the strategy, we may loop on assets using multithreading, was asking simple strategy : it cant lose
