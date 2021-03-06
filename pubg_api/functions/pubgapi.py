import requests
import pandas as pd
from scipy import stats
from chicken_dinner.pubgapi import PUBG

z_label = (["dbnos", "assists", "boosts", "damage_dealt", "heals", "kill_streaks", "kills", "longest_kill", "revives", "ride_distance", "swim_distance", "headshot_kills", "vehicle_destroys", "walk_distance", "weapons_acquired"])

def get_tournament_info(api_key):
    # Get the list of available tournaments
    url = "https://api.pubg.com/tournaments"
    header = {"Authorization": api_key, "Accept": "application/vnd.api+json"}
    # tournament_list를 json으로 호출
    r = requests.get(url, headers=header)
    tournament_list = r.json()

    # tournament_id, createdAt 값 추출
    tournament_id = []
    tournament_createdAt = []
    for i in range(len(tournament_list["data"])):
        temp_id = tournament_list["data"][i]["id"]
        temp_createdAt = tournament_list["data"][i]["attributes"]["createdAt"]
        tournament_id.append(temp_id)
        tournament_createdAt.append(temp_createdAt)

    tournament_info = pd.DataFrame(tournament_id, columns=["id"])
    tournament_info["createdAt"] = tournament_createdAt
    return tournament_info

def get_match_info(api_key, idx):
    pubg = PUBG(api_key, "pc-tournament")
    tournaments = pubg.tournaments()
    tournament = tournaments[idx]

    current_tournament = tournament.response

    # 해당 tournament_id의 모든 match_id와 created_at을 dict으로 출력
    matchId_dict = {match["attributes"]["createdAt"]: match["id"] for match in current_tournament["included"]}

    # matchId_dict를 createdAt로 정렬 후 dataframe으로 변환
    match_info = pd.DataFrame(sorted(matchId_dict.items(), key=lambda x: x[0]), columns=["createdAt", "matchId"])

    return match_info

def get_match_participant(api_key, match_info_id):
    # match의 모든 id값을 받아서 append
    PUBG_prime = PUBG(api_key=api_key, shard="pc-tournament", gzip=True)
    # match_participant
    player_id = []
    team_roster_id = []
    team_id = []
    team_rank = []
    match_id = []
    participant_stats = []

    # match_participant 값 입력
    for i in match_info_id:
        match = PUBG_prime.match(i)
        rosters = match.rosters
        for j in range(len(rosters)):
            roster = rosters[j]
            roster_participant = roster.participants
            for k in range(len(roster_participant)):
                participant = roster_participant[k]
                match_id.append(match.id)
                player_id.append(participant.name)
                team_roster_id.append(roster.id)
                team_rank.append(roster.stats['rank'])
                team_id.append(roster.stats['team_id'])
                stats = participant.stats
                participant_stats.append(stats)

    # Dataframe 생성
    match_participant = pd.DataFrame({'match_id': match_id, 'player_id': player_id, 'team_roster_id': team_roster_id, 'team_id': team_id, 'team_rank': team_rank})
    match_participant_stats = pd.DataFrame(participant_stats).drop(columns='player_id')

    # 인덱스 기준으로 join
    match_participant_all = pd.merge(match_participant, match_participant_stats, how="inner", left_index=True, right_index=True)

    # 불필요한 column 제거
    result_match_participant = match_participant_all.drop(["team_kills", "death_type", "kill_place", "name", "road_kills", "team_roster_id", "team_id", "vehicle_destroys", "weapons_acquired", "win_place"], axis='columns')

    return result_match_participant

def get_match_participant_single(api_key, match_info_id):
    # 단일 id 받아서 해당 경기만 출력
    PUBG_prime = PUBG(api_key=api_key, shard="pc-tournament", gzip=True)
    # match_participant
    player_id = []
    team_roster_id = []
    team_id = []
    team_rank = []
    match_id = []
    participant_stats = []

    # match_participant 값 입력
    match = PUBG_prime.match(match_info_id)
    rosters = match.rosters
    for i in range(len(rosters)):
        roster = rosters[i]
        roster_participant = roster.participants
        for j in range(len(roster_participant)):
            participant = roster_participant[j]
            match_id.append(match.id)
            player_id.append(participant.name)
            team_roster_id.append(roster.id)
            team_rank.append(roster.stats['rank'])
            team_id.append(roster.stats['team_id'])
            stats = participant.stats
            participant_stats.append(stats)

    # Dataframe 생성
    match_participant = pd.DataFrame({'match_id': match_id, 'player_id': player_id, 'team_roster_id': team_roster_id, 'team_id': team_id, 'team_rank': team_rank})
    match_participant_stats = pd.DataFrame(participant_stats).drop(columns='player_id')

    # 인덱스 기준으로 join
    match_participant_all = pd.merge(match_participant, match_participant_stats, how="inner", left_index=True, right_index=True)

    # round_point column 추가
    round_point = []
    team_point_rule = {1:10, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1, 8:1}

    for k in range(len(match_participant_all["win_place"])):
        team_rank = match_participant_all["win_place"][k]
        kill_point = match_participant_all["kills"][k]
        if team_rank in team_point_rule.keys():
            team_point = team_point_rule[team_rank]
        else:
            team_point = 0
        round_point.append(team_point + kill_point)

    match_participant_all["round_point"] = round_point

    # win column 추가
    match_participant_all["win"] = 1 * (match_participant_all["win_place"] == 1)

    # 불필요한 column 제거
    result_match_participant_single = match_participant_all.drop(["time_survived", "road_kills", "team_kills", "death_type", "kill_place", "name", "team_roster_id", "team_id", "win_place"], axis='columns')

    return result_match_participant_single

def z_normalization(match_participant_single):
    # Z-score normalization
    # z_label = (["dbnos", "assists", "boosts", "damage_dealt", "heals", "kill_streaks", "kills", "longest_kill", "revives", "ride_distance", "swim_distance", "headshot_kills", "vehicle_destroys", "walk_distance", "weapons_acquired"])
    
    for i in z_label:
        match_participant_single[i] = stats.zscore(match_participant_single[i])

    match_participant_single.drop(["player_id", "team_rank", "match_id"], axis = 1, inplace = True)

    return match_participant_single

def standard_scaling(df):
    scale_columns = (["dbnos", "assists", "boosts", "damage_dealt", "heals", "kill_streaks", "kills", "longest_kill", "revives", "ride_distance", "swim_distance", "headshot_kills", "vehicle_destroys", "walk_distance", "weapons_acquired"])
    for col in scale_columns:
        series_mean = df[col].mean()
        series_std = df[col].std()
        df[col] = df[col].apply(lambda x: (x-series_mean)/series_std)
    return df

def check_missing_value(filename, df):
    # 결측치가 발생한 부분에서 log 파일(.csv) 생성
    if (df.isnull().sum()).sum() != 0:
        df.to_csv(f"./Data/Error_log/{filename}.csv")
        raise Exception(f"Missing value: {(df.isnull().sum()).sum()}\nCheck Error_log: pubg_api/Data/Error_log/{filename}.csv")