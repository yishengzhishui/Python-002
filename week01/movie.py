import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
myurl = 'https://maoyan.com/films?showType=3'

# headers 加入 cookies 否则容易限制ip反扒
header = {
    'Cookie': '__mta=108886717.1595746864015.1595746990576.1595750256786.5; uuid_n_v=v1; uuid=C4064090CF0D11EA84945F632DCF0A4D8D0B8CE986ED4FA1A5DF764899054947; _csrf=cc22244000e0cb4545dc4fba39835376bd716a9dfb32352439a8183eea8eaff7; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595746863; _lxsdk_cuid=17389ecc837c8-0451626c3d648-15356650-13c680-17389ecc837c8; _lxsdk=C4064090CF0D11EA84945F632DCF0A4D8D0B8CE986ED4FA1A5DF764899054947; mojo-uuid=f5014f1d514958ccd91c2b07fb1ddc88; mojo-session-id={"id":"67b05808821b4609886449918e6ec14a","time":1596375047953}; mojo-trace-id=10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1596377754; __mta=108886717.1595746864015.1595750256786.1596377754746.6; _lxsdk_s=173af5e1f30-5db-992-85b%7C%7C19',
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
