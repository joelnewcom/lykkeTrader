import time
import lykke_trader.repository
import lykke_history.librarian
import matplotlib.pyplot as plt
import numpy as np


def price_is_still_higher(history_asset_pair):
    pass


def is_raising(slope):
    return slope > 0


def is_falling(slope):
    return slope < 0


def get_trend(ask):
    simple_index = list(np.arange(0, len(ask)))
    pl = np.polyfit(simple_index, ask, 1)
    return float(pl[0])


class Trader(lykke_trader.repository.Repository, lykke_history.librarian.Librarian):

    def __init__(self, repository: lykke_trader.repository.Repository, known_assets_ids,
                 librarian: lykke_history.librarian.Librarian):
        self.repository = repository
        self.librarian = librarian
        self.known_assets_ids = known_assets_ids
        self.trend_to_compare_in_days = 8
        self.max_money_per_buy = 50
        self.min_money_to_spend = 10
        self.percentage_of_data_points_to_check = 30

    def run(self):
        for asset_pair_id in self.known_assets_ids:
            self.buy_procedure(asset_pair_id)

    def buy_procedure(self, asset_pair="XRPCHF"):

        dates, ask, bid = self.librarian.read_history_file(asset_pair)

        # just show it:
        plt.plot(dates, ask, "ob", label="ask price")
        plt.xticks(rotation=90)
        plt.plot(dates, ask, "-b")

        how_many_data_points = len(ask)
        if how_many_data_points < self.librarian.how_long_back_in_time_days:
            print("asset pair: {} has only {} ask datapoints".format(asset_pair, how_many_data_points))
            return

        how_many_data_points_to_check_at_the_end = max(2, round(
            how_many_data_points / 100 * self.percentage_of_data_points_to_check))

        print("We check {} data points out of {} data points".format(how_many_data_points_to_check_at_the_end,
                                                                     how_many_data_points))
        simple_index = list(np.arange(0, len(ask)))
        pl = np.polyfit(simple_index, ask, 1)
        plt.plot(simple_index, np.polyval(pl, simple_index), "-r", label="polynomial fitted linear equation")

        simple_index = list(np.arange(len(ask) - how_many_data_points_to_check_at_the_end, len(ask)))
        pl = np.polyfit(simple_index, ask[len(ask) - how_many_data_points_to_check_at_the_end:len(ask)], 1)
        plt.plot(simple_index, np.polyval(pl, simple_index), "-g",
                 label="polynomial fitted linear equation last two points")

        plt.title("asset_pair: {}".format(asset_pair))
        plt.legend()
        plt.show()

        slope_over_all_data_points = get_trend(ask)
        slope_of_last_two_data_points = get_trend(ask[len(ask) - how_many_data_points_to_check_at_the_end:len(ask)])

        balance = self.repository.get_balance("CHF")
        print("money to spend: {}".format(balance))
        if balance > self.min_money_to_spend and is_falling(slope_over_all_data_points) and is_raising(
                slope_of_last_two_data_points):
            money_to_spend = min(balance, self.max_money_per_buy)
            asset_pair_rate = self.repository.get_asset_pairs_rate(asset_pair)
            ask = asset_pair_rate["ask"]
            if ask is not None:
                volume = 1 / float(ask) * money_to_spend
            print("Decision to buy {} for {} CHF, volume: {}".format(asset_pair, money_to_spend, volume))
            self.repository.limit_order_buy(asset_pair, volume,ask)

    def trenddetector(self, list_of_index, array_of_data, order=1):
        result = np.polynomial.polynomial.Polynomial.fit(list_of_index, list(array_of_data), order)
        slope = result[-2]

        # if the slope is a +ve value --> increasing trend
        # if the slope is a -ve value --> decreasing trend
        # if the slope is a zero value --> No trend
        return float(slope)
