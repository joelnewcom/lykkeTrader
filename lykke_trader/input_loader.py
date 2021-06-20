import json
import configparser
from jsonpath_ng import parse
from lykke_trader.repository import Repository
from typing import List
from typing import Dict
from lykke_trader.asset_pair import AssetPair


class InputLoader:

    def __init__(self, ini_file):

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

        self.known_available_asset_pairs = self.get_available_asset_pairs_refactored(dictionary_response,
                                                                                     known_asset_pair_ids)

    @staticmethod
    def get_available_asset_pairs(dictionary_response, known_asset_pair_ids: List[str]):
        available_asset_pair_ids = []
        for match in parse('[*].id').find(dictionary_response):
            available_asset_pair_ids.append(match.value)
        print(f'Possible asset pairs are: {available_asset_pair_ids}')
        known_available_asset_pairs = []
        for known_asset_pair_id in known_asset_pair_ids:
            if known_asset_pair_id not in available_asset_pair_ids:
                print(f'Given asset pair is not available: "{known_asset_pair_id}" and will be ignored')
            else:
                known_available_asset_pairs.append(known_asset_pair_id)
        if not known_available_asset_pairs:
            raise Exception("At least one available asset pair must be configured in the ini config file")

        return known_available_asset_pairs

    @staticmethod
    def get_available_asset_pairs_refactored(dictionary_response, known_asset_pair_ids: List[str]) \
            -> Dict[str, AssetPair]:
        available_asset_pair_ids: Dict[str, AssetPair] = {}

        for asset in dictionary_response:
            if known_asset_pair_ids.__contains__(asset["id"]):
                available_asset_pair_ids[asset["id"]] = AssetPair(asset["id"], asset["name"], asset["accuracy"],
                                                                  asset["invertedAccuracy"], asset["baseAssetId"],
                                                                  asset["quotingAssetId"])

        if len(available_asset_pair_ids) != len(known_asset_pair_ids):
            for known_asset_pair_id in known_asset_pair_ids:
                if not available_asset_pair_ids.__contains__(known_asset_pair_id):
                    print(f'Given asset pair is not available: "{known_asset_pair_id}" and will be ignored')
        return available_asset_pair_ids

    def get_repository(self):
        return self.repository

    def get_api_key(self):
        return self.api_key

    def get_known_asset_pairs(self):
        return self.known_available_asset_pairs
