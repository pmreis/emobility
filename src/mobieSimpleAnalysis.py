import pandas as pd

BASE_DATA_SOURCE_PATH = "data/sources"
BASE_DATA_OUTPUT_PATH = "data/outputs"

mobieJsonData = f"{BASE_DATA_SOURCE_PATH}/mobie_locations.json"

df = pd.read_json(mobieJsonData)
dfnorm = pd.json_normalize(df["data"])
total_rows = dfnorm.shape[0]

simpleAnalisys = dfnorm["party_id"].value_counts().reset_index()
simpleAnalisys.columns = ["party_id", "count"]
simpleAnalisys = simpleAnalisys.assign(pos=lambda _: _.index + 1, mrkt_shr=lambda _: _["count"] / total_rows)
simpleAnalisys = simpleAnalisys.assign(mrkt_shr_acc=simpleAnalisys["mrkt_shr"].cumsum())
simpleAnalisys.insert(0, "idx", simpleAnalisys.pop("pos"))
simpleAnalisys.to_csv(f"{BASE_DATA_OUTPUT_PATH}/simpleAnalysis.csv", sep=";", index=None, mode="w")
