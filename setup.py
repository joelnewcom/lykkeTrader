from lykke_history.librarian import Librarian
from lykke_trader.input_loader import InputLoader
from lykke_trader.trader import Trader

inputLoader = InputLoader('./config.ini')
librarian = Librarian(inputLoader.repository, inputLoader.known_available_asset_pairs)

trader = Trader(inputLoader.repository, inputLoader.known_available_asset_pairs, librarian)
trader.run()
