import configparser
import json
from trader.trader import Trader
from trader.repository import Repository

config = configparser.ConfigParser()
config.read('../config.ini')
config.sections()

api_key = config.get("DEFAULT", "apiKey")
known_assets_ids = json.loads(config.get("DEFAULT", "knownAssetsIds"))

repository = Repository(api_key, known_assets_ids)
trader = Trader(repository)
trader.run()
