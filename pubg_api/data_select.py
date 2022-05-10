import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

# RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")

# mariaDB와 connect
conn = pymysql.connect(host=endpoint, user=username, passwd=password, database=dbname, port=3306, charset='utf8')
cur = conn.cursor()

# SHOW(cur를 통해서 sql문을 주고 받는다.)
cur.execute("SHOW COLUMNS FROM match_participant")
result = cur.fetchall()
result = pd.DataFrame(result)
print(result)

# SELECT(cur를 통해서 sql문을 주고 받는다.)
cur.execute("SELECT * FROM tournament_info")
result = cur.fetchall()
result = pd.DataFrame(result)
print(result)

# db접속 종료
conn.close()