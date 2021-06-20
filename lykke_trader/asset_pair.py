class AssetPair:
    id = "string",
    name = "string",
    accuracy = 0,
    invertedAccuracy = 0,
    baseAssetId = "string",
    quotingAssetId = "string"

    def __init__(self, id: str, name: str, accuracy: int, invertedAccuracy: int, baseAssetId: str, quotingAssetId: str):
        self.id = id
        self.name = name
        self.accuracy = accuracy
        self.invertedAccuracy = invertedAccuracy
        self.baseAssetId = baseAssetId
        self.quotingAssetId = quotingAssetId
