import time
import lykke_trader.repository
import lykke_history.librarian
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def price_is_still_higher(history_asset_pair):
    pass


class Trader(lykke_trader.repository.Repository, lykke_history.librarian.Librarian):

    def __init__(self, repository: lykke_trader.repository.Repository, known_assets_ids,
                 librarian: lykke_history.librarian.Librarian):
        self.repository = repository
        self.librarian = librarian
        self.known_assets_ids = known_assets_ids
        self.trend_to_compare_in_days = 3
        self.max_money_per_buy = 50
        self.min_money_to_spend = 10

    def run(self):
        volumeTraded = 50
        assetTraded = "CHF"
        frequency_in_seconds = 2

        paid_price = self.librarian.getPaidPrice("XRPCHF")
        dates, ask, bid = self.librarian.get_history_asset_pair("XRPCHF")

        # Bid = Others want to buy at this price
        bid, ask = self.repository.order_book_asset("XRPCHF")

        # Sell to highest buy, Buy at lowest ask
        highest_bid = max([i["Price"] for i in bid])
        lowest_ask = min([i["Price"] for i in ask])

        trend = self.trenddetector()

        if self.isFalling(bid) and price_is_still_higher(highest_bid):
            self.limit_order_sell("XRPCHF", 50)

        # spread = highest bid - lowest ask
        spread = highest_bid - lowest_ask

        # We then look if we can buy lower than maxiSell or sell higher than maxiBuy
        # if buyAvalable < maxiSell and notBuyYet:
        # notBuyYet = not self.repository.marketOrder(assetTraded, "Buy", volumeTraded)

        # if sellAvalable > miniBuy and notSellYet:
        # notSellYet = not self.repository.marketOrder(assetTraded, "Sell", volumeTraded)

        time.sleep(frequency_in_seconds)

    def buy_procedure(self, asset_pair="XRPCHF"):
        # balance = self.repository.get_balance("CHF")
        # print("money to spend: {0}".format(balance))

        # asset_pair_rates = self.repository.get_asset_pairs_rate(asset_pair)

        dates, ask, bid = self.librarian.read_history_file(asset_pair)
        self.isRaising(dates, ask)

        # if balance > self.min_money_to_spend and self.isRaising(dates, ask):
        #     money_to_spend = min(balance, self.max_money_per_buy)
        # self.repository.limit_order_buy("XRPCHF", money_to_spend)

    def shouldSell(self, story_asset_pair):
        return False

    def isRaising(self, dates, ask):
        l = list(np.arange(0, len(ask)))
        pl = np.polynomial.polynomial.Polynomial.fit(l, ask, 1)
        pl = np.polyfit(l, ask, 1)

        # m = pl.coef[0]
        # b = pl.coef[1]

        # datesTrend = np.linspace(0, len(ask), len(ask))
        # price_trend_line = m * datesTrend + b

        plt.plot(dates, ask, "o")
        plt.plot(l, np.polyval(pl, l))
        plt.show()

    def isFalling(self, history_asset_pair):
        pass

    def trenddetector(self, list_of_index, array_of_data, order=1):
        result = np.polynomial.polynomial.Polynomial.fit(list_of_index, list(array_of_data), order)
        slope = result[-2]
        return float(slope)

        # if the slope is a +ve value --> increasing trend
        # if the slope is a -ve value --> decreasing trend
        # if the slope is a zero value --> No trend

        pass
