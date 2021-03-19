import configparser
import json
from lykke_trader.trader import Trader
from lykke_trader.repository import Repository
from lykke_history.librarian import Librarian

from jsonpath_ng import jsonpath, parse

config = configparser.ConfigParser()
ini_file = './config.ini'
config.read(ini_file)
config.sections()

api_key = config.get("DEFAULT", "apiKey")
if api_key is None:
    print("apiKey is missing in " + ini_file)

repository = Repository(api_key)

knownAssetsIdIniValue = config.get("DEFAULT", "knownAssetsIds")
if knownAssetsIdIniValue is None:
    print("No assetIds configured in " + ini_file)

known_assets_ids = json.loads(knownAssetsIdIniValue)

if not repository.is_alive():
    raise Exception("Lykke server is not reachable")

dictionary = repository.get_dictionary_assetpairs_spot()
jsonpath_expression = parse('[*].id')
for match in jsonpath_expression.find(dictionary):
    print(f'Employee id: {match.value}')

librarian = Librarian(repository, known_assets_ids)
librarian.write_history_file()
librarian.show_history_file()

#trader = Trader(repository, known_assets_ids)
#trader.run()
