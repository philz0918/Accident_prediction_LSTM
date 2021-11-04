
import pandas as pd
import matplotlib.pyplot as plt

#%matplotlib inline
## functions forformatting data 

'''
Frequency by month depends on key
'''

def get_dist_month_yandk(df,year,key) :
    jan_cnt = 0
    feb_cnt = 0 
    mar_cnt = 0
    apr_cnt = 0 
    may_cnt = 0 
    jun_cnt = 0
    jul_cnt = 0
    aug_cnt = 0
    sep_cnt = 0
    ocb_cnt = 0
    nov_cnt = 0
    dec_cnt = 0
    none_cnt = 0
    year = str(year)
    df = df.loc[df['year']==year]
    df.index = range(len(df))
    #print(len(df))
    #print(df.head(20))
    for i in range(len(df)) :
        if df.loc[i,"month"] =='january' :
            #print(type(df.loc[i,"bodies"]))
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    jan_cnt +=1
                else :
                    jan_cnt +=1
        elif df.loc[i,"month"] =='february' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    feb_cnt +=1
                else :
                    feb_cnt +=1
        elif df.loc[i,"month"] =='march' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    mar_cnt +=1
                else :
                    mar_cnt +=1
                
        elif df.loc[i,"month"] =='april' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    apr_cnt +=1
                else :
                    apr_cnt +=1
        elif df.loc[i,"month"] =='may' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    may_cnt +=1
                else :
                    may_cnt +=1
        elif df.loc[i,"month"] =='june' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    jun_cnt +=1
                else :
                    jun_cnt +=1
        elif df.loc[i,"month"] =='july' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    jul_cnt +=1
                else :
                    jul_cnt +=1
        elif df.loc[i,"month"] =='august' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    aug_cnt +=1
                else :
                    aug_cnt +=1
        elif df.loc[i,"month"] =='september' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    sep_cnt +=1
                else :
                    sep_cnt +=1
        elif df.loc[i,"month"] =='october' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    ocb_cnt +=1
                else :
                    ocb_cnt +=1
        elif df.loc[i,"month"] =='november' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    nov_cnt +=1
                else :
                    nov_cnt +=1
        elif df.loc[i,"month"] =='december' :
            if key in df.loc[i,"body"] :
                if key =='collapsed' and 'fell' not in df.loc[i,"body"] :
                    dec_cnt +=1
                else :
                    dec_cnt +=1
        else :
                none_cnt +=0
    
    fin_set_mon = {}
    fin_set_mon[year+'-01'] = jan_cnt
    fin_set_mon[year+'-02'] = feb_cnt
    fin_set_mon[year+'-03'] = mar_cnt
    fin_set_mon[year+'-04'] = apr_cnt
    fin_set_mon[year+'-05'] = may_cnt
    fin_set_mon[year+'-06'] = jun_cnt
    fin_set_mon[year+'-07'] = jul_cnt
    fin_set_mon[year+'-08'] = aug_cnt
    fin_set_mon[year+'-09'] = sep_cnt
    fin_set_mon[year+'-10'] = ocb_cnt
    fin_set_mon[year+'-11'] = nov_cnt
    fin_set_mon[year+'-12'] = dec_cnt
    fin_set_mon['none'] = none_cnt
    
    
    return fin_set_mon


def gen_ts_data(df_arrange, keyword) :
    dist_yandk={}
    total_list=[]
    t_value=[]
    
    for yr in range(2000, 2020) :
        dist_yandk[yr] = get_dist_month_yandk(df_arrange,yr, keyword)
        total_list.extend(list(dist_yandk[yr])[:-1])
        t_value.extend(list(dist_yandk[yr].values())[:-1])
    
    # dates,values 
    return total_list, t_value

def trans_date(dates) :
    n_dates = dates.to_pydatetime()
    date_list = []
    
    for i in range(len(n_dates)) :
        date_list.append(n_dates[i].strftime('%Y-%m-%d'))
    
    #formatted date_list['2019-12-31']
    return date_list

def convert_df(dates, values) :
    df = pd.DataFrame({'date': dates, 'freq' : values})
    df['date']  = pd.to_datetime(df['date'], format = '%Y-%m-%d')
    df = df.set_index('date')
    
    return df

#plotting for train and test
# return train and test 

def naive_plot(df) :
    
    df['freq'].plot()
    
    return 

def plotting(df) :
    
    #80percent point
    split_date = pd.Timestamp('31-12-2015')

    train = df.loc[:split_date, ['freq']]
    test = df.loc[split_date:, ['freq']]

    ax = train.plot()
    test.plot(ax=ax)
    
    #plt.yscale('log')
    plt.legend(['train', 'test'])
    
    return train, test

if __name__ == "__main__":
    dates = pd.date_range('2000-01-01', '2019-12-31', freq='M')
    dates= trans_date(dates)

    # get timeseries data -fire, fell, struck

    _, fire_value = gen_ts_data(df_arrange, 'fire')
    df_fire = convert_df(dates,fire_value )
    naive_plot(df_fire)
    fire_train, fire_test = plotting(df_fire)

    '''
    _, fell_value = gen_ts_data(df_arrange, 'fell')
    df_fell = convert_df(dates, fell_value)
    naive_plot(df_fell)
    fell_train, fell_test = plotting(df_fell)


    _, struck_value = gen_ts_data(df_arrange, 'struck')
    df_struck = convert_df(dates, struck_value)
    naive_plot(df_struck)
    struck_train, struck_test = plotting(df_struck)
    
    '''