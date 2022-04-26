import requests
import json
import pandas as pd
from chicken_dinner.pubgapi import PUBG

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

def get_match_info(api_key, tournament_id):
    # 해당 tournament_id를 불러오기 위한 link 작성
    url = f"https://api.pubg.com/tournaments/{tournament_id}"
    header = {"Authorization": api_key, "Accept": "application/vnd.api+json"}
    
    # tournament_list를 json으로 호출
    r = requests.get(url, headers=header)
    current_tournament = r.json()

    # 모든 match_id와 created_at을 dict으로 출력
    matchId_dict = {match['attributes']['createdAt']: match['id'] for match in current_tournament['included']}

    # matchId_dict를 createdAt로 정렬 후 dataframe으로 변환
    match_info = pd.DataFrame(sorted(matchId_dict.items(), key=lambda x: x[0]), columns=['createdAt', 'matchId'])

    return match_info

def get_match_participant(api_key, match_info_id):
    PUBG_prime = PUBG(api_key=api_key, shard='pc-tournament', gzip=True)
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
    match_participant_all = pd.merge(match_participant, match_participant_stats, how='inner', left_index=True, right_index=True) 

    # 불필요한 column 제거
    result_match_participant = match_participant_all.drop(['match_id', 'death_type', 'kill_place', 'name', 'ride_distance', 'road_kills', 'swim_distance', 'team_roster_id', 'team_id', 'vehicle_destroys', 'walk_distance', 'weapons_acquired', 'win_place'], axis='columns')

    return result_match_participant


def get_match_info2(api_key, tournament_id):
    # 해당 tournament_id를 불러오기 위한 link 작성
    url = f"https://api.pubg.com/tournaments/{tournament_id}"
    header = {"Authorization": api_key, "Accept": "application/json"}

    # tournament_list를 json으로 호출
    r = requests.get(url, headers=header)
    current_tournament = json.loads(r.text)

    # 모든 match_id와 created_at을 dict으로 출력
    matchId_dict = {match['attributes']['createdAt']: match['id'] for match in current_tournament['included']}

    # matchId_dict를 createdAt로 정렬 후 dataframe으로 변환
    match_info = pd.DataFrame(sorted(matchId_dict.items(), key=lambda x: x[0]), columns=['createdAt', 'matchId'])

    return match_info