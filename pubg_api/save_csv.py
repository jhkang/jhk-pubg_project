# Reference
# https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

import pandas as pd
import requests
import pymysql
import json
import os
from dotenv import load_dotenv
from chicken_dinner.pubgapi import PUBG
from functions.pubgapi import get_tournament_info
from functions.pubgapi import get_match_info
from functions.pubgapi import get_match_participant

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")

# PUBG class를 토너먼트용 class로 custom
PUBG_prime = PUBG(api_key=api_key, shard='pc-tournament', gzip=True)

# Tournament id 값 조회
tournament_info = get_tournament_info(api_key)
tournament_id = tournament_info["id"]

print(f"{len(tournament_id)} 개의 tournament_id 조회 완료")


# Save match_info to csv file
for idx in range(0, 1):
    tournament_index_id = tournament_id[idx]
    cur_match_info = get_match_info(api_key, tournament_index_id)
    num_match = len(cur_match_info["matchId"])

    match_info_id = cur_match_info["matchId"]
    match_participant = get_match_participant(api_key, match_info_id)
    match_participant.to_csv(f"./Data/{tournament_index_id}_match_info.csv")
    print(f"Tournament name {idx}: {tournament_index_id} ({num_match} matches)")
print("complete")