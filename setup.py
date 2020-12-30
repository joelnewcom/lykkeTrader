import configparser
import json
from lykke_trader.trader import Trader
from lykke_trader.repository import Repository
from lykke_history.librarian import Librarian

config = configparser.ConfigParser()
config.read('./config.ini')
config.sections()

api_key = config.get("DEFAULT", "apiKey")
known_assets_ids = json.loads(config.get("DEFAULT", "knownAssetsIds"))

repository = Repository(api_key)

if not repository.is_alive():
    raise Exception("Lykke server is not reachable")

librarian = Librarian(repository, known_assets_ids)
librarian.run()



#trader = Trader(repository, known_assets_ids)
#trader.run()
