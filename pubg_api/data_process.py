from dotenv import load_dotenv
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from functions.pubgapi import get_tournament_info
from functions.pubgapi import get_match_info
from functions.pubgapi import get_match_participant_single
from functions.pubgapi import standard_scaling
from functions.pubgapi import check_missing_value
import pandas as pd
import os

# Load api key & RDS info (endpoint="rds 엔드포인트", dbname="db 이름", username="마스터 사용자 이름", password="rds 비밀번호")
load_dotenv()
api_key = os.environ.get("API_KEY")
endpoint = os.environ.get("AWS_endpoint")
dbname = os.environ.get('AWS_dbname')
username = os.environ.get("AWS_username")
password = os.environ.get("AWS_password")

# tournament_info(.csv) 불러오기
tournament_info = pd.read_csv("./DB/tournament_info.csv")
tournament_info.drop(["Unnamed: 0"], axis = 1, inplace = True)
check_missing_value('tournament_info', tournament_info)

loading_bar = {0:'-', 1:'\\', 2:'|', 3:'/'}
for tournament_index in range(len(tournament_info["id"])):
    # index 설정 및 해당 인덱스의 tournament_id 값 불러오기
    tournament_name = tournament_info["id"][tournament_index]
    tournament_createdAt = tournament_info["createdAt"][tournament_index]

    # cur_match_info(Current match info) 불러오기
    cur_match_info = get_match_info(api_key, tournament_index)

    # match_participant_single 불러오기
    for match_index in range(len(cur_match_info["matchId"])):
        match_participant_single = get_match_participant_single(api_key, cur_match_info["matchId"][match_index])
        check_missing_value(cur_match_info["matchId"][match_index], match_participant_single)

        # Z-score normalization 수행
        # data = z_normalization(match_participant_single)
        data = match_participant_single

        if os.path.isfile("./Data/Train_data/train_match_data.csv"):
            # 해당 경로에 train_match_data.csv 파일이 있으면, 현재 내용을 해당 파일에 추가
            train_data = pd.read_csv(f"./Data/Train_data/train_match_data.csv")
            train_data.drop(["Unnamed: 0"], axis = 1, inplace = True)
            train_data = pd.concat([train_data, data], ignore_index=True)
            train_data.to_csv(f"./Data/Train_data/train_match_data.csv")
        else:
            # 해당 경로에 train_match_data.csv 파일이 없으면, 파일 생성
            data.to_csv(f"./Data/Train_data/train_match_data.csv")
        print(f"\rLoading tournament data {loading_bar[match_index%4]}", end="")

data = pd.read_csv(f"./Data/Train_data/train_match_data.csv")
data.drop(["Unnamed: 0", "match_id", "player_id"], axis = 1, inplace = True)

#######################
#  Linear Regression  #  round_point 획득량 예상 -> mvp 지표로 사용 가능
#######################
X = data[data.columns.difference(['round_point', 'win'])]
y = data['round_point']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=19)

# 회귀 분석 객체 생성(선형 회귀 모델 생성)
lr = linear_model.LinearRegression()

lr_model = lr.fit(X_train, y_train)

x_new=X_test
y_new=lr_model.predict(x_new)

print("\n<Linear Regression>")
print("훈련 세트 정확도 : {:.3f}".format(lr_model.score(X_train,y_train)))
print("테스트 세트 정확도 : {:.3f}\n".format(lr_model.score(X_test,y_test)))

y_compare={'y_test':y_test, 'y_predicted':y_new}
pd.DataFrame(y_compare)[:30].plot(y=['y_test', 'y_predicted'], alpha=0.6, kind="bar")

#######################
#    Random Forest    #  win_feature -> 우승 예측
#######################
rf_data = standard_scaling(data)
z_label = (["dbnos", "assists", "boosts", "damage_dealt", "heals", "kill_streaks", "kills", "longest_kill", "revives", "ride_distance", "swim_distance", "headshot_kills", "vehicle_destroys", "walk_distance", "weapons_acquired"])
X = rf_data[z_label]
y = rf_data["win"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

forest = RandomForestClassifier(n_estimators=50, random_state=0)
forest.fit(X_train,y_train)

print("<Random Forest>")
print("훈련 세트 정확도 : {:.3f}".format(forest.score(X_train,y_train)))
print("테스트 세트 정확도 : {:.3f}".format(forest.score(X_test,y_test)))