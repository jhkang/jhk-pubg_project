import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from functions.pubgapi import get_tournament_info
from functions.pubgapi import get_match_info
from functions.pubgapi import check_missing_value

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")

##############
# DB connect #   create_engine("mysql+pymysql://아이디:"+"암호"+"@주소:포트/데이터베이스이름?charset=utf8", encoding='utf-8')
##############

engine = create_engine("mysql+pymysql://admin:"+password+"@"+endpoint+":3306/"+dbname+"?charset=utf8", encoding="utf-8")
conn = engine.connect()

# 각 tournament 별 match 정보 조회 & 저장
tournament_info = pd.read_csv("./DB/tournament_info.csv")
tournament_info.drop(["Unnamed: 0"], axis = 1, inplace = True)
check_missing_value("tournament_info", tournament_info)

tournament_id = tournament_info["id"]
num_tournament = len(tournament_id)

for tournament_idx in range(num_tournament):
    cur_match_info = get_match_info(api_key, tournament_idx)
    cur_match_info.insert(loc=0, column="tournamentId", value=f"{tournament_id[tournament_idx]}")

    if os.path.isfile("./DB/match_info.csv"):
        # 해당 경로에 match_info.csv 파일이 있으면, 현재 내용을 해당 파일에 추가
        match_info = pd.read_csv(f"./DB/match_info.csv")
        match_info.drop(["Unnamed: 0"], axis = 1, inplace = True)
        match_info = pd.concat([match_info, cur_match_info], ignore_index=True)
        match_info.to_csv(f"./DB/match_info.csv")
    else:
        # 해당 경로에 match_info.csv 파일이 없으면, 파일 생성
        cur_match_info.to_csv(f"./DB/match_info.csv")

# db접속 종료
conn.close()