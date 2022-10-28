import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

def get_lianjia_ershoufang(url='https://sh.lianjia.com/ershoufang/', page=1):
    time_get_data = date.today()
    city = url[8:10]
    #print(city, time_get_data)
    if page>1:
        url = url + 'pg' + str(page) + '/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    house_list = soup.find_all( class_ = "info clear" )
    house_data = []
    for it in house_list:
        #sub_soup = BeautifulSoup(it, 'html.parser')
        title = it.find(class_="title").get_text().strip()
        flood = it.find(class_="flood").get_text().strip()
        address = it.find(class_="address").get_text().strip()
        followInfo = it.find(class_="followInfo").get_text().strip()
        tag = it.find(class_="tag").get_text().strip()
        priceInfo = it.find(class_="priceInfo").get_text().strip()
        """
        st = ""
        st = st + title + "\n"
        st = st + flood + "\n"
        st = st + address + "\n"
        st = st + followInfo + "\n"
        st = st + tag + "\n"
        st = st + priceInfo
        tuple_data = st
        """
        tuple_data = ( time_get_data, city, title, flood, address, followInfo, tag, priceInfo )
        house_data.append( tuple_data )
    return house_data

def get_data_by_city(city='bj'):
    url='https://' + city + '.lianjia.com/ershoufang/'
    time_get_data = date.today()
    house_data = []
    try:
        for i in range(1, 501):
            page=i
            tmp = get_lianjia_ershoufang(url, page)
            house_data += tmp
            if i%10==0:
                print(city, page, len(tmp), len(house_data))
            if len(tmp)==0:
                break
    except:
        print('cannot connect to website')
    df_data = pd.DataFrame(house_data, columns =['time_get_data', 'city', 'title', 'flood', 'address', 'followInfo', 'tag', 'priceInfo'])
    df_data[['follower','release_time']] = df_data['followInfo'].str.split("/", expand=True) # 
    df_data['release_time'] = df_data['release_time'].str.strip()
    return df_data


time_get_data = date.today()
city_list = ['bj', 'sh', 'sz', 'gz', 'hz', 'nj', 'dg', 'wh', 'cd', 'xa']
city = 'gz'
for city in city_list[:]:
    df_data = get_data_by_city(city)
    file_name = str(time_get_data) + "_" + str(city) + '.csv'
    df_data.to_csv("C:/Users/Admin/Desktop/"+file_name) # save file
    print(file_name, len(df_data))
    

