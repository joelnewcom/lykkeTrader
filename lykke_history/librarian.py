import os
import time
from datetime import date

import dateutil.relativedelta
import matplotlib.pyplot as plt
import numpy as np
from lykke_trader.asset_pair import AssetPair
from typing import List
from typing import Dict

DATA_FILE_HEADER = "date, ask price, bid price"

data_file_delimiter = ','
waitingTimeInSec = 11


class Librarian:
    how_long_back_in_time_days = 8
    one_day = dateutil.relativedelta.relativedelta(days=1)

    def __init__(self, repository, known_assets_ids: Dict[str, AssetPair]):
        self.asset_pairs_history = {}
        self.repository = repository
        self.known_assets_ids: Dict[str, AssetPair] = known_assets_ids
        self.update_history_files()

    def update_history_files(self):
        for asset_pair_dictionary in self.known_assets_ids.values():
            dates, ask, bid = self.read_history_file(asset_pair_dictionary.id)
            if dates and len(dates) >= self.how_long_back_in_time_days:
                newest_date_in_file = dates[len(dates) - 1]
                newest_date_in_file_as_date = date.fromisoformat(newest_date_in_file)
                next_date_after_newest_date_in_file = newest_date_in_file_as_date + dateutil.relativedelta.relativedelta(
                    days=1)
                self.append_history_file_newest_date_last(asset_pair_dictionary.id, next_date_after_newest_date_in_file)
            else:
                os.remove(asset_pair_dictionary.id + '_data.csv')
                oldest_date_to_start_history = date.today() - dateutil.relativedelta.relativedelta(
                    days=Librarian.how_long_back_in_time_days)
                self.append_history_file_newest_date_last(asset_pair_dictionary.id, oldest_date_to_start_history)

    def append_history_file_newest_date_last(self, asset_pair, next_date):
        file_path = asset_pair + '_data.csv'

        with open(file_path, "a") as data_file:

            if os.stat(file_path).st_size == 0:
                data_file.write("%s\n" % DATA_FILE_HEADER)

            today = date.today()
            while today >= next_date:

                history_rates = self.repository.get_history_rate(asset_pair, next_date.strftime('%Y-%m-%d'), "day")

                if history_rates["ask"] is not None and history_rates["bid"] is not None:
                    print("ask price: " + str(history_rates["ask"]) + " other price: " +
                          str(history_rates["ask"]) + " for assetId: " + asset_pair)
                    data_file.write(str(next_date) + "," +
                                    str(history_rates["ask"]) + "," +
                                    str(history_rates["bid"]) + "\n")

                next_date = next_date + self.one_day
                time.sleep(waitingTimeInSec)

    @staticmethod
    def read_history_file(asset_pair):
        file_path = asset_pair + '_data.csv'

        if not os.path.isfile(file_path):
            return [], [], []

        with open(file_path, "r") as data_file:

            line_values = []

            # check for header
            first_line = data_file.readline()
            if first_line and not first_line.startswith(DATA_FILE_HEADER):
                line_values.append(first_line.strip().split(data_file_delimiter))

            while True:
                line = data_file.readline()
                # if line is empty end of file is reached
                if not line:
                    break
                line_values.append(line.strip().split(data_file_delimiter))

        dates = [item[0].strip() for item in line_values]
        ask = [float(item[1].strip()) for item in line_values]
        bid = [float(item[2].strip()) for item in line_values]

        return dates, ask, bid

    def plot_history_file(self, asset_pair):
        dates, ask, bid = self.read_history_file(asset_pair)

        plt.plot(dates, ask)
        plt.gcf().autofmt_xdate()
        plt.show()

        plt.plot(dates, bid)
        plt.gcf().autofmt_xdate()
        plt.show()

    @staticmethod
    def get_history_asset_pair(asset_pair):
        return np.loadtxt(fname=asset_pair + '_values.csv', delimiter=',')

    @staticmethod
    def file_len(file_handle):
        count = 0
        for _ in file_handle:
            count += 1
        return count
