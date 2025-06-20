import pandas as pd
import os.path as osp
import os
from pathlib import Path

BASE_DATA_PATH = Path(
    os.getenv("DATA_SOURCE_PATH", Path(__file__).resolve().parent.parent / "data")
)

mobieInPath = osp.normpath(f"{BASE_DATA_PATH}/sources/mobie_locations.json")
analysisOutPath = osp.normpath(f"{BASE_DATA_PATH}/outputs/PT_Market_Share_Analysis.csv")

df = pd.read_json(mobieInPath)
dfnorm = pd.json_normalize(df["data"])
total_rows = dfnorm.shape[0]

simpleAnalisys = dfnorm["party_id"].value_counts().reset_index()
simpleAnalisys.columns = ["party_id", "count"]
simpleAnalisys = simpleAnalisys.assign(pos=lambda _: _.index + 1, mrkt_shr=lambda _: _["count"] / total_rows)
simpleAnalisys = simpleAnalisys.assign(mrkt_shr_acc=simpleAnalisys["mrkt_shr"].cumsum())
simpleAnalisys.insert(0, "idx", simpleAnalisys.pop("pos"))
simpleAnalisys.to_csv(analysisOutPath, sep=",", index=None, mode="w")
