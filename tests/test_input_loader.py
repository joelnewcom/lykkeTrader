import unittest

from lykke_trader import input_loader
from lykke_trader import repository


class TestInputLoader(unittest.TestCase):
    def test_get_asset_pairs_rate(self):
        dict_spot = repository.Repository.get_dictionary_asset_pairs_spot()
        known_asset_pair_ids = ["BCHCHF", "BTCCHF", "LKKCHF", "LKK2YCHF", "XLMCHF",
                                "XRPCHF", "ETHCHF"]
        result = input_loader.InputLoader.get_available_asset_pairs_refactored(dict_spot,
                                                                               known_asset_pair_ids)
        self.assertEqual(len(result), len(known_asset_pair_ids))


if __name__ == '__main__':
    unittest.main()
