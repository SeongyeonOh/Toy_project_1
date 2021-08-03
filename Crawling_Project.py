# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# 시즌별 득점 순위, 선수이름, 팀명, 득점수 # (가능하면 도움수까지)

# https://sports.news.naver.com/wfootball/record/index?category=epl&year=2020&tab=player

# 위의 인터넷 페이지 주소를 규칙화 하기. 첫번째 가장 중요한 포인트
# 시즌과 리그별로 달라지는 부분이 존재함을 확인

# 해당 페이지의 page source를 직접 가져와서 체크. 웹페이지에서도 우클릭 "페이지 소스 보기"로 HTML 소스 확인가능

import bs4
from urllib.request import urlopen
import pandas as pd
import numpy as np
import re

# 시즌과 리그정보를 주면 페이지마다 필요한 정보들(선수 이름, 소속팀, 득점수)를 크롤링 + 순위만들기
def crawl_naver_sports(league,year):
    naver_sports = f"https://sports.news.naver.com/wfootball/record/index?category={league}&year={year}&tab=player"
    source=urlopen(naver_sports).read() #웹페이지에 들어가서 소스들을 .read()로 가져온다
    source=bs4.BeautifulSoup(source,'lxml') #lxml로 열기
    
    # 소스에서 선수 이름이 포함된 부분을 모두 찾아 리스트로 반환
    span=source.find_all('span',class_='name')[-20:] #마지막 indexing은 시즌 득점왕 같은 중복정보가 들어가서 그 부분을 빼주기 위함

    # 소속팀 리스트
    span2=source.find_all('span',class_='team')[-20:]

    # 득점수 리스트
    span3=source.find_all('td',class_='selected')

    # 선수 이름만 뽑아서 리스트 만들기 #ex.디디에 드록바, 로빈 반 페르시
    name_list=[]
    for name in range(len(span)):
        name_list.append(span[name].text)
# 굳이 아래처럼 길게 할 필요가 없어서 주석
#     for name in span:
#         k_name=re.findall('[가-힣]+[\s]*[가-힣]+[\s]*[가-힣]+',str(name))
#         #print(k_name)
#         name_list.append(k_name[0])


    
    # 소속팀만 뽑아서 리스트 만들기
    team_list=[]
    for team in range(len(span2)):
        team_list.append(span2[team].text)
#     for team in span2:
#         k_team=re.findall('[가-힣]+',str(team))
#         #print(k_name)
#         team_list.append(k_team[0])
    

    
    # 득점수만 뽑아서 리스트 만들기
    goal_list=[]
    for goal in span3:
        k_goal=re.findall('[0-9]+',str(goal))
        #print(k_goal)
        goal_list.append(k_goal[0]) #이중리스트라 [0]을 해줘야함
    
    # 순위를 크롤링 하는 것보다는 직접 골수를 비교해서 순위를 매겨주는 코드를 짜고 싶어서 넣음.
    # 기록이 동률일때는 같은 순위로 만들고 (다음 순위) = (이전순위)+(같은 순위인 선수의 수) 인 순위 리스트 만들기.
    rank_list=[1]
    rank=1
    same_rank_count=1

    for i in range(len(goal_list)-1):
        if goal_list[i]==goal_list[i+1]:
            rank_list.append(rank)
            same_rank_count+=1
        else:
            rank+=same_rank_count
            same_rank_count=1
            rank_list.append(rank)
        
    # 순위/선수이름/소속팀/득점수 : 해당 리스트들을 넣은 dataframe생성 후 반환
    df=pd.DataFrame({"순위":rank_list,"선수명":name_list,"소속팀":team_list,"득점수":goal_list})
    return df


# 네이버에서 제공하는 5개의 리그와 시즌 리스트
league_list = ['epl','primera','bundesliga','seria','ligue1']
year_list = range(2009,2021)

# 특정 리그의 해당 시즌 득점랭킹을 dataframe으로 만들어 csv파일로 각각 저장
for y in range(len(year_list)):
    for l in range(len(league_list)):
        # 예외처리
        try:
            data=crawl_naver_sports(league_list[l],year_list[y])
        except:
            print("Error")
        #print(data)
        
        data.to_csv(f'../K-Digital Training/Crawling_Data/{year_list[y]}_{league_list[l]}_score_ranking.csv')

# -

# - 에러 발생에 대비해야 한다.
#
#
# - 중간중간 저장을 하거나, 에러케이스에서 예외처리를 하는 식으로 발생할 문제에 대처해야한다.


