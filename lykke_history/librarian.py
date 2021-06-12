import os
import time
from datetime import date

import dateutil.relativedelta
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE_HEADER = "date, ask price, bid price"

data_file_delimiter = ','
waitingTimeInSec = 11


class Librarian:
    # 2 years = 730
    how_long_back_in_time_days = 8
    one_day = dateutil.relativedelta.relativedelta(days=1)

    def __init__(self, repository, known_assets_ids):
        self.asset_pairs_history = {}
        self.repository = repository
        self.known_assets_ids = known_assets_ids
        self.update_history_files()

    def update_history_files(self):
        for asset_pair_id in self.known_assets_ids:
            dates, ask, bid = self.read_history_file(asset_pair_id)
            if dates and len(dates) >= self.how_long_back_in_time_days:
                newest_date_in_file = dates[len(dates) - 1]
                newest_date_in_file_as_date = date.fromisoformat(newest_date_in_file)
                next_date_after_newest_date_in_file = newest_date_in_file_as_date + dateutil.relativedelta.relativedelta(
                    days=1)
                self.append_history_file_newest_date_last(asset_pair_id, next_date_after_newest_date_in_file)
            else:
                os.remove(asset_pair_id + '_data.csv')
                oldest_date_to_start_history = date.today() - dateutil.relativedelta.relativedelta(
                    days=Librarian.how_long_back_in_time_days)
                self.append_history_file_newest_date_last(asset_pair_id, oldest_date_to_start_history)

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

    def write_history_files_newest_date_last(self):
        for asset_pair_id in self.known_assets_ids:
            self.write_history_file_newest_date_last(asset_pair_id)

    def write_history_file_newest_date_last(self, asset_pair_id):
        today = date.today()

        data_file = open(asset_pair_id + '_data.csv', "w")
        data_file.write("%s\n" % DATA_FILE_HEADER)
        for days_going_back in range(self.how_long_back_in_time_days, 0, -1):
            moving_time_window = today - dateutil.relativedelta.relativedelta(days=days_going_back)
            formatted_date = moving_time_window.strftime('%Y-%m-%d')

            print("requested date: " + str(formatted_date) + " for assetId: " + asset_pair_id)
            history_response = self.repository.get_history_rate(asset_pair_id, formatted_date, "day")

            if history_response["ask"] is not None and history_response["bid"] is not None:
                print("ask price: " + str(history_response["ask"]) + " other price: " +
                      str(history_response["ask"]) + " for assetId: " + asset_pair_id)
                data_file.write(str(formatted_date) + "," +
                                str(history_response["ask"]) + "," +
                                str(history_response["bid"]) + "\n")

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
