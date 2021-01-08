import os.path
import time
from datetime import datetime

import dateutil.relativedelta
import matplotlib.pyplot as plt
import numpy as np


class Librarian:
    # 2 years = 730
    how_long_back_in_time_days = 3
    one_day = dateutil.relativedelta.relativedelta(days=1)

    def __init__(self, repository, known_assets_ids):
        self.repository = repository
        self.known_assets_ids = known_assets_ids

    def write_history_file(self):
        time_window = datetime.today()

        for asset_id in self.known_assets_ids:
            date_times = np.empty(shape=0, dtype='datetime64')
            values = np.empty(shape=0)

            # Check the existing file.
            file_name = asset_id + '_data.csv'

            number_of_lines = 0
            date_first_entry = datetime.today()

            if not os.path.isfile(file_name):
                new_file = open(file_name, "a")
                new_file.close()

            with open(file_name, "r") as file:
                number_of_lines = self.file_len(file)
            print(number_of_lines)

            if number_of_lines == 0:
                date_first_entry = datetime.today()
            else:
                with open(file_name, "r") as file:
                    first_entry_in_file = file.readline()
                    print("first_entry_in_file: " + first_entry_in_file)
                    date_first_entry = datetime.fromisoformat(first_entry_in_file)

            # Prepend to file
            date_delta = datetime.today() - date_first_entry

            if date_delta.days > 1:


            # print("Difference now - last entry" + (time_window - parsed_date_time))

            # first_date_time is not yesterday
            # now = datetime.datetime.now()
            # np.datetime64(str(now))
            # for i in range(self.how_long_back_in_time_days):
            #     # Format if working with date_time: time_window.strftime('%Y-%m-%dT00:00:00.000')[:-3] + "Z"
            #     formatted_date = time_window.strftime('%Y-%m-%d')
            #
            #     print("requested date: " + str(formatted_date))
            #     history_response = self.repository.get_history(asset_id, formatted_date)
            #
            #     date_times = np.append(date_times, np.datetime64(str(time_window)))
            #     values = np.append(values, history_response["ask"])
            #     print("ask price: " + str(history_response["ask"]) + "other price: " + str(history_response["ask"]))
            #     time_window = time_window - self.one_day
            #     time.sleep(11)
            #
            # np.savetxt(fname=asset_id + '_values.csv', X=values, delimiter=',')
            # np.savetxt(fname=asset_id + '_date_times.csv', X=date_times, fmt='%s', delimiter=',')

    def show_history_file(self):
        values = np.loadtxt(fname='XRPCHF' + '_values.csv', delimiter=',')
        date_times = np.loadtxt(fname='XRPCHF' + '_date_times.csv', dtype='datetime64', delimiter=',')

        plt.plot(date_times, values)
        plt.show()

    @staticmethod
    def file_len(file_handle):
        count = 0
        for _ in file_handle:
            count += 1
        return count
