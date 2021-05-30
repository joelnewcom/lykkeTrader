from lykke_history.librarian import Librarian
from lykke_trader.input_loader import InputLoader
from lykke_trader.trader import Trader

inputLoader = InputLoader('./config.ini')
librarian = Librarian(inputLoader.repository, inputLoader.known_available_asset_pairs)
# librarian.plot_history_file('XRPCHF')

# Globals
amountToSpendAtOneTime = 50
waitingTimeInMilliSec = 1000

trader = Trader(inputLoader.repository, inputLoader.known_available_asset_pairs, librarian)
trader.buy_procedure('XRPCHF')
