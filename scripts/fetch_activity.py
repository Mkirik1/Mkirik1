"""Fetches the last 12 months of contributions via the GitHub GraphQL API
and writes data/activity.json for the XP card. Needs GITHUB_TOKEN."""
import json, os, urllib.request
from collections import OrderedDict
from datetime import date
from pathlib import Path

USER = os.environ.get("GH_USER", "Mkirik1")
q = {"query": "query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}",
     "variables": {"u": USER}}
req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(q).encode(),
                             headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
months = OrderedDict()
best = cur = 0
for d in days:
    dt = date.fromisoformat(d["date"])
    key = dt.strftime("%Y-%m")
    months.setdefault(key, {"label": dt.strftime("%b").upper(), "count": 0})
    months[key]["count"] += d["contributionCount"]
    cur = cur + 1 if d["contributionCount"] else 0
    best = max(best, cur)
out = {"total": cal["totalContributions"], "streak": best, "months": list(months.values())[-12:]}
Path(__file__).resolve().parent.parent.joinpath("data", "activity.json").write_text(json.dumps(out, indent=1))
print(out["total"], "contributions")
