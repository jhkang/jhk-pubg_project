Design evaluation indicators based on PUBG E-Sports data.
=============
PUBG E-Sports 데이터를 활용한 정량적 평가지표 설계 프로젝트

## .env 파일 설정 방법
`jhk-pubg_project/.env` 경로에 `.env` 파일을 생성한다.
```
# PUBG API KEY
API_KEY = "your api key"

# AWS RDS info
AWS_endpoint = "your endpoint link"
AWS_dbname = "your database name"
AWS_username = "your username"
AWS_password = "your password"
```
PUBG API KEY에는 발급받은 API KEY를 입력한다. </br>
AWS RDS info에는 발급받은 AWS RDS 정보를 입력한다.

## Dockerfile 설정
WSL2 & Docker Desktop 설치 : [Get started with Docker remote containers on WSL 2](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers) <br/> <br/>
`jhk-pubg_project/`로 디렉토리를 변경한 후에 docker container를 생성하고 실행한다. <br/>
ex) docker container name: `pubg_dockerfile`
```
docker build --tag pubg_dockerfile:0.1 .
docker create -it --rm --name pubg_dockerfile pubg_dockerfile:0.1
docker start pubg_dockerfile
docker exec -it pubg_dockerfile bash
```
Docker container를 중지하고 그에 해당하는 이미지를 제거하고자 하는 경우에는 아래와 같이 실행
```
docker stop pubg_dockerfile
docker rmi pubg_dockerfile:0.1
```

## Python 파일 실행

|Filename|Description|
|---|---|
|savecsv_tournament.py|Make tournament_info.csv|
|savecsv_match.py|Make match_info.csv|
|savecsv_participant.py|Make match_participant.csv|
```
python savecsv_tournament_info.py
python savecsv_match_info.py
python savecsv_participant.py
```


## 참고자료
* [PUBG Developer Portal](https://developer.pubg.com/)
* [배틀그라운드 e스포츠 데이터 분석](https://github.com/dataitgirls4/team_5)
* [chicken-dinner](https://github.com/crflynn/chicken-dinner)
