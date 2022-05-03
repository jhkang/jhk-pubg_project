import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from functions.pubgapi import get_tournament_info
from functions.pubgapi import get_match_info
from functions.pubgapi import get_match_participant_single
from functions.pubgapi import get_match_participant

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")


# Tournament id 값 조회
tournament_info = get_tournament_info(api_key)
tournament_id = tournament_info["id"]

print(f"{len(tournament_id)} 개의 tournament_id 조회 완료\n")


# Save match_info to csv file
for idx in range(0, 1):
    # idx를 지정하여 해당 위치의 id값 출력
    tournament_index_id = tournament_id[idx]
    cur_match_info = get_match_info(api_key, tournament_index_id)
    num_match = len(cur_match_info["matchId"])

    match_info_id = cur_match_info["matchId"]
    match_participant = get_match_participant(api_key, match_info_id)
    match_participant.to_csv(f"./Data/{tournament_index_id}_match_info.csv")
    print(f"Tournament name {idx}: {tournament_index_id} ({num_match} matches)")
print("complete")

# Match participant 조회
idx2 = 2
match_info_id = cur_match_info["matchId"]
match_info_id_single = match_info_id[idx2]
match_participant = get_match_participant_single(api_key, match_info_id_single)


# DB와 connect

# create_engine("mysql+pymysql://아이디:"+"암호"+"@주소:포트/데이터베이스이름?charset=utf8", encoding='utf-8')
engine = create_engine("mysql+pymysql://admin:"+password+"@"+endpoint+":3306/"+dbname+"?charset=utf8", encoding="utf-8")
conn = engine.connect()

# AWS RDS에 테이블 create

if match_participant["kills"].sum() != 0:
    # Kill 수의 합이 0인 경우 제외(연습게임으로 간주)
    match_participant.to_sql(name="train_match_data", con=conn, if_exists='append', index=False)

# 업로드된 테이블 확인
sql = "SHOW TABLES;"
result = pd.read_sql(sql, conn)
print(sql)

# 내용 확인(SELECT *)
sql = f"SELECT * FROM train_match_data;"
result1 = pd.read_sql(sql, conn)
print(sql)

# db접속 종료
conn.close()