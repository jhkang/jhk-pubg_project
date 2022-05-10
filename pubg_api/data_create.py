import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")

# DB connect

# create_engine("mysql+pymysql://아이디:"+"암호"+"@주소:포트/데이터베이스이름?charset=utf8", encoding='utf-8')
engine = create_engine("mysql+pymysql://admin:"+password+"@"+endpoint+":3306/"+dbname+"?charset=utf8", encoding="utf-8")
conn = engine.connect()

# 테이블 read
tournament_info = pd.read_csv(f"./DB/tournament_info.csv", index_col = 0)
match_info = pd.read_csv(f"./DB/match_info.csv", index_col = 0)
match_participant = pd.read_csv(f"./DB/match_participant.csv", index_col = 0)
print(tournament_info)

# 테이블 create
tournament_info.to_sql(name="tournament_info", con=conn, if_exists='replace', index=False)
match_info.to_sql(name="match_info", con=conn, if_exists='replace', index=False)
match_participant.to_sql(name="match_participant", con=conn, if_exists='replace', index=False)

conn.close()