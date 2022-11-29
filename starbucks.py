import pandas as pd
import folium
import warnings
import matplotlib
import matplotlib.pyplot as plt
from haversine import haversine


warnings.filterwarnings(action="ignore")
matplotlib.rc("font", family="AppleGothic")
matplotlib.rc("axes", unicode_minus=False)
# csv 파일 read
temp = pd.read_csv("소상공인시장진흥공단_상가(상권)정보_커피점카페_서울_202209.csv", encoding="utf-8")

# 원하는 column만
data_columns = ["상가업소번호", "상호명", "지점명", "상권업종대분류명", "상권업종중분류명", "시도명", "시군구명", "행정동명", "경도", "위도"]
data = temp[data_columns]

# 상권업종중분류명이 커피점/카페 인 곳
df_coffee = data[data["상권업종중분류명"] == "커피점/카페"]
df_coffee.index = range(len(df_coffee))

# 스타벅스 주변에 cafes 매장이 얼마나 있는지 분석 및 map 에 위치 표시
def analysis_of_cafes_around_starbucks(cafes):
    # 상호명에 스타벅스 가 포함되는 곳
    df_starbucks = df_coffee[df_coffee["상호명"].str.contains("스타벅스")]
    # df_starbucks.index = range(len(df_starbucks))
    print("서울 스타벅스 점포 수 :", len(df_starbucks))

    # 상호명에 cafes 가 포함되는 곳
    df_cafes = df_coffee[df_coffee["상호명"].str.contains(cafes)]
    # df_cafes.index = range(len(df_cafes))
    print(f"서울 {cafes} 매장 수 :", len(df_cafes))

    # 중심 지정
    lat = df_starbucks["위도"].mean()
    long = df_starbucks["경도"].mean()

    # map 에 위치 표시
    starbucks_cafes_distance_analysis_map = folium.Map(
        [lat, long],
        zoom_start=11,
        tiles="OpenStreetMap"
    )

    cafes_around_starbucks_count = 0
    starbucks_distance = 50

    for x in df_starbucks.index:
        for y in df_cafes.index:
            starbucks_lat = df_starbucks.loc[x, "위도"]
            starbucks_long = df_starbucks.loc[x, "경도"]
            starbucks_title = df_starbucks.loc[x, "지점명"]

            cafes_lat = df_cafes.loc[y, "위도"]
            cafes_long = df_cafes.loc[y, "경도"]
            cafes_title = df_cafes.loc[y, "지점명"]

            if haversine((starbucks_lat, starbucks_long), (cafes_lat, cafes_long), unit="m") < starbucks_distance:
                folium.CircleMarker(
                    [starbucks_lat, starbucks_long],
                    color="green",
                    radius=4,
                    tooltip=starbucks_title
                ).add_to(starbucks_cafes_distance_analysis_map)
                folium.CircleMarker(
                    [cafes_lat, cafes_long],
                    color="blue",
                    radius=4,
                    tooltip=cafes_title
                ).add_to(starbucks_cafes_distance_analysis_map)
                cafes_around_starbucks_count += 1

    starbucks_cafes_distance_analysis_map.save(f"result/스타벅스_{cafes}_{starbucks_distance}_analysis_cmark.html")

    print(f"스타벅스와 {cafes} 지점간 거리가 {starbucks_distance}m 이내 인 수 :",
          cafes_around_starbucks_count,
          f"\n서울 {cafes} 매장 중 스타벅스 근처 {starbucks_distance}m 이내에 있는 비율 :",
          cafes_around_starbucks_count / len(df_cafes) * 100, "%"
          )

# 서울 구 별로 카페 갯수를 visualization
def cafes_visualization(cafes):
    df_cafes = df_coffee[df_coffee["상호명"].str.contains(cafes)]
    plt.figure(figsize=(20, 6))
    plt.title(f"서울의 {cafes} 분포", fontdict={"fontsize": 15})
    plt.bar(df_cafes["시군구명"].value_counts().index, df_cafes["시군구명"].value_counts().values)
    plt.xticks(rotation="horizontal")
    plt.savefig(f"{cafes}_barplot.png")


cafes_visualization("스타벅스")

analysis_of_cafes_around_starbucks("이디야")
analysis_of_cafes_around_starbucks("투썸플레이스")
analysis_of_cafes_around_starbucks("메가커피")
analysis_of_cafes_around_starbucks("컴포즈커피")
analysis_of_cafes_around_starbucks("빽다방")
analysis_of_cafes_around_starbucks("커피에반하다")
analysis_of_cafes_around_starbucks("요거프레소")
analysis_of_cafes_around_starbucks("커피베이")
analysis_of_cafes_around_starbucks("더벤티")

"""
공정거래위원회 내 가맹점 수 TOP 10
국내 커피 브랜드 별 매장수
1  이디야
2  스타벅스
3  투썸플레이스
4  메가커피
5  컴포즈커피
6  빽다방
7  커피에반하다
8  요거프레소
9  커피베이
10 더벤티
"""
