import json
import configparser
from jsonpath_ng import parse
from lykke_trader.repository import Repository


class InputLoader:

    def __init__(self, ini_file):

        json_path_expression = parse('[*].id')
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.sections = config.sections()

        self.api_key = config.get("DEFAULT", "apiKey")
        if self.api_key is None:
            raise Exception("Mandatory apiKey is missing in " + ini_file)

        self.repository = Repository(self.api_key)

        known_asset_pair_ids_from_config = config.get("DEFAULT", "knownAssetsIds")

        if known_asset_pair_ids_from_config is None:
            raise Exception("At least one asset pair must be configured in: " + ini_file)

        known_asset_pair_ids = json.loads(known_asset_pair_ids_from_config)

        if not self.repository.is_alive():
            raise Exception("Lykke server is not reachable")

        dictionary_response = self.repository.get_dictionary_asset_pairs_spot()

        available_asset_pair_ids = []
        for match in json_path_expression.find(dictionary_response):
            available_asset_pair_ids.append(match.value)
        print(f'Possible asset pairs are: {available_asset_pair_ids}')

        self.known_available_asset_pairs = []
        for known_asset_pair_id in known_asset_pair_ids:
            if known_asset_pair_id not in available_asset_pair_ids:
                print(f'Given asset pair is not available: "{known_asset_pair_id}" and will be ignored')
            else:
                self.known_available_asset_pairs.append(known_asset_pair_id)

        if not self.known_available_asset_pairs:
            raise Exception("At least one available asset pair must be configured in: " + ini_file)

    def get_repository(self):
        return self.repository

    def get_api_key(self):
        return self.api_key

    def get_known_asset_pairs(self):
        return self.known_available_asset_pairs
