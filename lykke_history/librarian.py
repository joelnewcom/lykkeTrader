import json
import time
from datetime import datetime

import dateutil.relativedelta
import matplotlib.pyplot as plt
import datetime
import numpy as np


class Librarian:
    # 2 years = 730
    how_long_back_in_time_days = 30
    one_day = dateutil.relativedelta.relativedelta(days=1)

    def __init__(self, repository, known_assets_ids):
        self.repository = repository
        self.known_assets_ids = known_assets_ids

    def write_history_file(self):
        time_window = datetime.datetime.now()

        for asset_id in self.known_assets_ids:
            date_times = np.empty(shape=0, dtype='datetime64')
            values = np.empty(shape=0)

            for i in range(self.how_long_back_in_time_days):
                formatted_date_time = time_window.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
                print("requested date: " + str(formatted_date_time))
                history_response = self.repository.get_history(asset_id, formatted_date_time)
                date_times = np.append(date_times, np.datetime64(str(time_window)))
                values = np.append(values, history_response["ask"])
                print("ask price: " + str(history_response["ask"]) + "other price: " + str(history_response["ask"]))
                time_window = time_window - self.one_day
                time.sleep(11)

            np.savetxt(fname=asset_id + '_values.csv', X=values, delimiter=',')
            np.savetxt(fname=asset_id + '_date_times.csv', X=date_times, fmt='%s', delimiter=',')

    def show_history_file(self):
        values = np.loadtxt(fname='XRPCHF' + '_values.csv', delimiter=',')
        date_times = np.loadtxt(fname='XRPCHF' + '_date_times.csv', dtype='datetime64', delimiter=',')

        plt.plot(date_times, values)
        plt.show()