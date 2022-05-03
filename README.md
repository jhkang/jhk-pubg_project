PUBG E-Sports 데이터를 활용한 정량적 평가지표 설계 프로젝트
=============
Design evaluation indicators based on PUBG E-Sports data.
-------------

* 기간 : 2020.04.19 ~ in progress
* 목표 : Design evaluation indicators based on PUBG E-Sports data.

## How to run? (실행방법)
Change directory to jhk-pubg_project/
```
docker build --tag pubg_dockerfile:0.1 .

docker create -it --rm --name pubg_dockerfile pubg_dockerfile:0.1

docker start pubg_dockerfile

docker exec -it pubg_dockerfile bash
```
```
docker stop pubg_dockerfile

docker rmi pubg_dockerfile:0.1
```


## Reference Documentation
* [PUBG Developer Portal](https://developer.pubg.com/)
* [배틀그라운드 e스포츠 데이터 분석](https://github.com/dataitgirls4/team_5)
* [chicken-dinner](https://github.com/crflynn/chicken-dinner)
