Design evaluation indicators based on PUBG E-Sports data.
=============
PUBG E-Sports 데이터를 활용한 정량적 평가지표 설계 프로젝트

## Setup(.env)
Make `.env` file on `jhk-pubg_project/.env`
```
# PUBG API KEY
API_KEY = "your api key"

# AWS RDS info
AWS_endpoint = "your endpoint link"
AWS_dbname = "your database name"
AWS_username = "your username"
AWS_password = "your password"
```

## Setup(Dockerfile)
Install WSL2 & Docker Desktop: [Get started with Docker remote containers on WSL 2](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers) <br/> <br/>
Change directory to `jhk-pubg_project/` and create & run docker container. <br/>
ex) container name: `pubg_dockerfile`
```
docker build --tag pubg_dockerfile:0.1 .
docker create -it --rm --name pubg_dockerfile pubg_dockerfile:0.1
docker start pubg_dockerfile
docker exec -it pubg_dockerfile bash
```
Stop docker container and remove image (if you need)
```
docker stop pubg_dockerfile
docker rmi pubg_dockerfile:0.1
```


## Reference Documentation
* [PUBG Developer Portal](https://developer.pubg.com/)
* [배틀그라운드 e스포츠 데이터 분석](https://github.com/dataitgirls4/team_5)
* [chicken-dinner](https://github.com/crflynn/chicken-dinner)
