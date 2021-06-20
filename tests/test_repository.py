import unittest

from lykke_trader import repository


class TestPublicRepository(unittest.TestCase):
    def test_get_asset_pairs_rate(self):
        asset_pair = "BCHCHF"
        result = repository.Repository.get_asset_pairs_rate(asset_pair)
        self.assertEqual(result["id"], asset_pair)

    def test_get_version(self):
        result = repository.Repository.get_version()
        self.assertEqual(result["version"], "1.1.135.0")

    def test_is_alive(self):
        is_alive = repository.Repository.is_alive()
        self.assertTrue(is_alive)

    def test_get_dictionary_asset_pairs_spot(self):
        response = repository.Repository.get_dictionary_asset_pairs_spot()
        self.assertEqual(len(response), 160)


if __name__ == '__main__':
    unittest.main()
