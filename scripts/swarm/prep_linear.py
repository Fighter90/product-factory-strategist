#!/usr/bin/env python3
"""Одноразовая подготовка Linear для роя: метка `swarm`, навешивание на PRO-26…PRO-40, Backlog → Todo."""
import os, sys, json, pathlib, urllib.request

_keyfile = pathlib.Path.home() / ".swarm_linear_key"
KEY = os.environ.get("SWARM_LINEAR_KEY") or (_keyfile.read_text().strip() if _keyfile.exists() else "")
if not KEY:
    raise SystemExit("Нет ключа: задайте SWARM_LINEAR_KEY или создайте ~/.swarm_linear_key")
TEAM_KEY = "PRO"
ISSUES = [f"PRO-{n}" for n in range(26, 41)]

def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request("https://api.linear.app/graphql", data=body,
        headers={"Authorization": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    if d.get("errors"):
        raise SystemExit(f"GraphQL error: {d['errors'][0].get('message')}")
    return d["data"]

# 1) команда PRO и её состояния (root team(key:) нет в схеме — идём через organization)
org = gql('{ organization { teams { nodes { id key name } } } }')["organization"]["teams"]["nodes"]
team_id = next(t["id"] for t in org if t["key"] == TEAM_KEY)
team = gql('query($id:String!){ team(id:$id){ id states { nodes { id name } } } }', {"id": team_id})["team"]
states = {s["name"]: s["id"] for s in team["states"]["nodes"]}
todo_id, inprog_id, done_id = states.get("Todo"), states.get("In Progress"), states.get("Done")
assert todo_id and inprog_id and done_id, states

# 2) метка swarm (на команду)
label = gql('query($t:String!){ team(id:$t){ labels { nodes { id name } } } }', {"t": team_id})["team"]["labels"]["nodes"]
swarm = next((l for l in label if l["name"] == "swarm"), None)
if not swarm:
    swarm = gql('mutation($t:String!){ issueLabelCreate(input:{name:"swarm", color:"#64748b", description:"Автономный рой: оркестратор забирает задачу в работу", teamId:$t}){ issueLabel { id } } }', {"t": team["id"]})["issueLabelCreate"]["issueLabel"]
    print("метка swarm создана")
swarm_id = swarm["id"] if "id" in swarm else swarm["issueLabel"]["id"]

# 3) задачи: label + Todo (IssueFilter не умеет identifier — ищем по number)
for ident in ISSUES:
    num = int(ident.split("-")[1])
    q = gql('query($f:IssueFilter!){ issues(filter:$f, first:1){ nodes { id identifier title labels { nodes { id } } } } }',
            {"f": {"team": {"key": {"eq": TEAM_KEY}}, "number": {"eq": num}}})
    nodes = q["issues"]["nodes"]
    if not nodes:
        print(f"{ident}: НЕ НАЙДЕНА — пропуск"); continue
    iss = nodes[0]
    ids = [l["id"] for l in iss["labels"]["nodes"]]
    if swarm_id not in ids:
        ids.append(swarm_id)
    gql('mutation($id:String!,$labels:[String!],$state:String!){ issueUpdate(id:$id, input:{labelIds:$labels, stateId:$state}){ success } }',
        {"id": iss["id"], "labels": ids, "state": todo_id})
    print(f"{ident}: label=swarm + Todo ✓ ({iss['title'][:50]})")
print("готово — очередь роя готова")
