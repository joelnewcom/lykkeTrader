from trader import trader
import configparser
import json

config = configparser.ConfigParser()
config.read('../config.ini')
config.sections()
trader = trader(config.get("DEFAULT", "apiKey"), json.loads(config.get("DEFAULT", "knownAssetsIds")))
trader.run()
