import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
myurl = 'https://maoyan.com/films?showType=3'

# headers 加入 cookies 否则容易限制ip反扒
header = {
    'Cookie': 'HMACCOUNT=2209D7B5EF7944E2; BIDUPSID=E7B8AC5BBA402847A2905D6EB3DC7C0F; PSTM=1488176034; BDSFRCVID=3MIOJeCmH6a-Oj79qQQA8hLx6eKK0gOTHlx5LCgHa5q0bmDVJeC6EG0Ptf8g0KubkuYCogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tJFHoC8MfI03JJ7Gq4bMK4FQqxby26PeBm59aJ5nalP-Hj6OM6tBKq_uLH73Wnkq5m3ion3vQpnSJK5sLPJ1-jLLDM5L0p5Z5mAqKl0MLPbtbb0xynoDMnL4LUnMBMPj52OnaIQc3fAKftnOM46JehL3346-35543bRTohFLK-oj-D84j5LM3e; BAIDUID=74D3A9CA44A38ED688BFA7AD69E4982A:FG=1; BDUSS=VlISDd5UTJPeGpIa2p1N0ZBbUVNRkoxWW5vWGlydVpRWnZKVUNINGtCYXdvS05lSVFBQUFBJCQAAAAAAAAAAAEAAAApq0FZzsrOyjEyMzRsb3ZlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALATfF6wE3xeO; H_WISE_SIDS=142529_144497_142018_140631_145498_145871_144419_144135_145271_146537_146307_131247_144682_137743_144743_144251_141942_127969_146551_145805_140593_143492_145997_131423_128699_145909_146001_145351_107312_145287_146136_139909_144874_139882_146395_144966_145608_144762_145398_143856_139913_110085; ZD_ENTRY=google; delPer=0; PSINO=3; H_PS_PSSID=31731_1466_31671_21104_31605_31781_31271_30824_26350; BDUSS_BFESS=VlISDd5UTJPeGpIa2p1N0ZBbUVNRkoxWW5vWGlydVpRWnZKVUNINGtCYXdvS05lSVFBQUFBJCQAAAAAAAAAAAEAAAApq0FZzsrOyjEyMzRsb3ZlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALATfF6wE3xeO; HMACCOUNT_BFESS=2209D7B5EF7944E2; HMVT=fa218a3ff7179639febdb15e372f411c|1595746199|',
    'user-agent': user_agent}

response = requests.get(myurl, headers=header)
print(response.status_code)
bs_info = bs(response.text, 'html.parser')


# 处理字符串
def parse_text(str):
    return str.strip().split('\n')[-1].strip()


movie_infos = []
for tags in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
    movie_title, movie_category, movie_date = '', '', ''

    for tag in tags.find_all('div', attrs={'class': 'movie-hover-title'}):
        for i in tag.find_all('span', attrs={'class': 'hover-tag'}):
            if i.text == '类型:':
                movie_category = parse_text(i.find_parent('div').text)  # 获取节点的父节点的内容
            if i.text == '上映时间:':
                movie_date = parse_text(i.find_parent('div').text)
                movie_title = i.find_parent('div').get('title')  # 获取父节点的 属性内容
    movie_info = [movie_title, movie_category, movie_date]
    movie_infos.append(movie_info)

# 存储数据 csv 文件
df = pd.DataFrame(movie_infos[:10])
df.to_csv('./movie.csv', encoding='utf8', index=False, header=False)
