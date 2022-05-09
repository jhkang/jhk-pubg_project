import os
from dotenv import load_dotenv
from functions.pubgapi import get_tournament_info
from functions.pubgapi import check_missing_value

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")

# Tournament id 값 조회
tournament_info = get_tournament_info(api_key)
check_missing_value("tournament_info",tournament_info)
tournament_id = tournament_info["id"]
num_tournament = len(tournament_id)

print(f"{num_tournament}개의 tournament_id 조회 완료")

# Tournament info 테이블 저장(local)
tournament_info.to_csv(f"./DB/tournament_info.csv")
print(f"{num_tournament}개의 tournament_id 저장 완료")