import requests

API_KEY = "RGAPI-16b260f1-5a11-47de-b659-1e9b9c1f4592"  #from https://developer.riotgames.com
GAME_NAME = "KingHearts"  #Riot ID Name
TAG_LINE = "2487" #Riot ID tagline

REGION_ROUTING = "americas"
PLATFORM_ROUTING = "na1"
MATCH_COUNT = 5

headers = {"X-Riot-Token": API_KEY}

# GET PUUID from Riot ID

account_url = (
  f"https://{REGION_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
)

account_resp = requests.get(account_url, headers=headers)
print ("Account status:", account_resp.status_code)

if account_resp.status_code != 200:
  print("Account error:", account_resp.text)
  raise SystemExit

account_data = account_resp.json()
puuid = account_data["puuid"]

print(f"\nPlayer: {GAME_NAME}#{TAG_LINE}")
print(f"PUUID: {puuid}")

# GET Match IDs from PUUID (Last 5 matches)

match_ids_url = (
  f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/"
  f"matches/by-puuid/{puuid}/ids?start=0&count={MATCH_COUNT}"
)

match_ids_resp = requests.get(match_ids_url, headers=headers)
print("\nMatch IDs status:", match_ids_resp.status_code)

if match_ids_resp.status_code != 200:
  print("Match IDs error:", match_ids_resp.text)
  raise SystemExit

match_ids = match_ids_resp.json()

if not match_ids:
  print("No matches found for this player.")
  raise SystemExit

print(f"\nLast {len(match_ids)} matches: \n")

# Show stats from each match

for match_id in match_ids:
  match_url = (
    f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
  )

  match_resp = requests.get(match_url, headers=headers)
  print(f"Match {match_id} status:", match_resp.status_code)

  if match_resp.status_code != 200:
    print(" Error:", match_resp.text)
    continue

  match_data = match_resp.json()
  info = match_data["info"]
  participants = info["participants"]

  #Find Player in by puuid in match participants

  me = next((p for p in participants if p["puuid"] == puuid), None)
  if not me:
    print(" Player not found in match participants.")
    continue

  champ = me.get("championName", "Unknown")
  kills = me.get("kills", 0)
  deaths = me.get("deaths", 0)
  assists = me.get("assists", 0)
  win = me.get("win", False)

  result = "WIN" if win else "LOSS"
  queue_id = info.get("queueId", "Unknown")
  game_mode = info.get("gameMode", "Unknown")

  print("================================")
  print(f"Match ID: {match_id}")
  print(f"Ques ID: {queue_id}")
  print(f"Mode: {game_mode}")
  print(f"Champion: {champ}")
  print(f"K/D/A: {kills}/{deaths}/{assists}")
  print(f"Result: {result}")