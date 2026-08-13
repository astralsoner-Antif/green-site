#!/usr/bin/env python3
"""為替レート取得 → data/fx.json (JPY基準のCNY/USD)。
ビルド前に実行するとサイトの参考換算が更新される。常時更新は不要(Koki方針)。"""
import json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import datetime
d = json.load(urllib.request.urlopen("https://open.er-api.com/v6/latest/JPY", timeout=20))
iso = datetime.datetime.utcfromtimestamp(d["time_last_update_unix"]).strftime("%Y-%m-%d")
fx = {
    "cny": d["rates"]["CNY"],
    "usd": d["rates"]["USD"],
    "date_iso": iso,
}
json.dump(fx, open(os.path.join(ROOT, "data", "fx.json"), "w"), indent=1)
print(fx)
