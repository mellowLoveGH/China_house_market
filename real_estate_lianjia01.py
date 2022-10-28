import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_path="C:/Users/Admin/Desktop/2022-10-27_sh.csv"):
    df_data = pd.read_csv(file_path, index_col=0)
    df_data[['follower','release_time']] = df_data['followInfo'].str.split("/", expand=True) # 
    df_data['release_time'] = df_data['release_time'].str.strip()
    df_data[ ['whole_price', 'unit_price'] ] = df_data['priceInfo'].str.split('万', expand=True)
    #df_data['whole_price'] = df_data['whole_price'].astype(float)
    df_data['unit_price'] = df_data['unit_price'].str[:-3]
    df_data['unit_price'] = df_data['unit_price'].str.replace(',', '')
    df_data['unit_price'] = df_data['unit_price'].astype(int)
    return df_data

def daily_str():
    tmp = []
    for day_num in range(1, 32):
        tmp.append( str(day_num)+'天以前发布' )
    return tmp

def monthly_str():
    tmp = []
    for month_num in range(1, 12):
        tmp.append( str(month_num)+'个月以前发布' )
    return tmp

def get_data_by_time(df_data, time_limit):
    tmp = df_data[ df_data['release_time']==time_limit ]
    col = list( tmp['unit_price'] )
    return col

def count_std(arr):
    if len(arr)<=0:
        return 0, 0
    avg, std = sum(arr)/len(arr), 0
    for v in arr:
        std = std + (v-avg)*(v-avg)
    return round(avg), round(std/len(arr))

###
daily_time = daily_str()
monthly_time = monthly_str()
#print( daily_time )
#print( monthly_time )

city_list = ['bj', 'sh', 'sz', 'gz', 'hz', 'nj', 'dg', 'wh', 'cd', 'xa']
for city in city_list[:]:
    file_path="C:/Users/Admin/Desktop/2022-10-27_" + city + ".csv"
    df_data = read_data(file_path)
    print( city, len(df_data) )
    current_month = []
    for day in daily_time:
        col = get_data_by_time(df_data, day)
        #avg = 0
        #if len(col)>0:
            #avg = sum(col)/len(col)
        #print(day, len(col), avg)
        current_month += col
    current_len = len(current_month)
    current_avg, current_std = count_std(current_month)
    print('0个月以前发布', current_len, current_avg, current_std)

    for month in monthly_time:
        col = get_data_by_time(df_data, month)
        avg, std = count_std(col)
        print(month, len(col), avg, std)





