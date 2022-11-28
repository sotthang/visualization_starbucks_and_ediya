import pandas as pd
import folium
import warnings
warnings.filterwarnings(action='ignore')
import matplotlib
matplotlib.rc('font', family='AppleGothic')
matplotlib.rc('axes', unicode_minus=False)
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

# csv 파일 read
temp = pd.read_csv("소상공인시장진흥공단_상가(상권)정보_커피점카페_서울_202209.csv", encoding='utf-8')

# 원하는 column만
data_columns = ['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '시군구명', '행정동명', '경도', '위도']
data = temp[data_columns]

# 상권업종중분류명이 커피점/카페 인 곳
df_coffee = data[data["상권업종중분류명"] == "커피점/카페"]
df_coffee.index = range(len(df_coffee))

# 상호명이 스타벅스 인 곳
df_starbucks = df_coffee[df_coffee["상호명"].str.contains("스타벅스")]
df_starbucks.index = range(len(df_starbucks))
print('전국 스타벅스 점포 수 :', len(df_starbucks))

'''
# 서울의 스타벅스 분포를 bar 형태로 visualization
plt.figure(figsize=(10, 6))
plt.title("서울의 스타벅스 분포", fontdict={"fontsize" : 20})
plt.bar(df_starbucks['시군구명'].value_counts().index, df_starbucks['시군구명'].value_counts().values)
plt.xticks(rotation='vertical')
# plt.xticks(rotation='horizontal')
plt.savefig("starbucks_barplot.png")
plt.show()
'''

# 중심 지정
lat = df_starbucks['위도'].mean()
long = df_starbucks['경도'].mean()

"""
starbucks_map = folium.Map(
    [lat, long],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# map 에 starbucks 위치 표시
for x in df_starbucks.index:
    sub_lat = df_starbucks.loc[x, '위도']
    sub_long = df_starbucks.loc[x, '경도']
    title = df_starbucks.loc[x, '지점명']
    folium.CircleMarker([sub_lat, sub_long], color='green', radius=4, tooltip=title).add_to(starbucks_map)

starbucks_map.save('starbucks_cmark.html')
"""

# 상호명이 이디야 인 곳
df_ediya = df_coffee[df_coffee["상호명"].str.contains("이디야")]
df_ediya.index = range(len(df_ediya))
print('전국 이디야 점포 수 :', len(df_ediya))


"""
# 서울의 이디야 분포를 bar 형태로 visualization
plt.figure(figsize=(10, 6))
plt.title("서울의 이디야 분포", fontdict={"fontsize" : 20})
plt.bar(df_ediya['시군구명'].value_counts().index, df_starbucks['시군구명'].value_counts().values)
plt.xticks(rotation='vertical')
# plt.xticks(rotation='horizontal')
plt.savefig("ediya_barplot.png")
plt.show()
"""

"""
ediya_map = folium.Map(
    [lat, long],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# map 에 ediya 위치 표시
for x in df_ediya.index:
    sub_lat = df_ediya.loc[x, '위도']
    sub_long = df_ediya.loc[x, '경도']
    title = df_ediya.loc[x, '지점명']
    folium.CircleMarker([sub_lat, sub_long], color='red', radius=4, tooltip=title).add_to(ediya_map)

ediya_map.save('ediya_cmark.html')
"""

starbucks_ediya_map = folium.Map(
    [lat, long],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# map 에 ediya 위치 표시
for x, y in zip(df_starbucks.index, df_ediya.index):
    starbucks_sub_lat = df_starbucks.loc[x, '위도']
    starbucks_sub_long = df_starbucks.loc[x, '경도']
    starbucks_title = df_starbucks.loc[x, '지점명']
    folium.CircleMarker(
        [starbucks_sub_lat, starbucks_sub_long],
        color='green',
        radius=4,
        tooltip=starbucks_title
    ).add_to(starbucks_ediya_map)

    ediya_sub_lat = df_ediya.loc[y, '위도']
    ediya_sub_long = df_ediya.loc[y, '경도']
    ediya_title = df_ediya.loc[y, '지점명']
    folium.CircleMarker(
        [ediya_sub_lat, ediya_sub_long],
        color='blue',
        radius=4,
        tooltip=ediya_title
    ).add_to(starbucks_ediya_map)

starbucks_ediya_map.save('starbucks_ediya_cmark.html')
