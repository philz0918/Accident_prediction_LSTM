
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pickle

'''
All token sentence from news articles body

1. Frequency of keywords
'''

#frequency of causation
def freq_keywords(token_sentences) :
    cnt_fire =0 
    cnt_fall =0
    cnt_collapse =0 
    cnt_crane = 0
    cnt_explosion = 0
    cnt_struck = 0
    cnt_caught = 0
    cnt_electrical = 0 

    for token in token_sentence :
        if 'fire' in token :
            cnt_fire +=1
        if 'collapsed' in token :
            if 'fell' not in token :
                cnt_fall +=1
            #print(token)
        if 'fell' in token :
            cnt_fall +=1
            #print(token)
        if 'crane' in token :
            cnt_crane +=1
            #print(token)
        if 'explosion' in token :
            cnt_explosion +=1
        if 'struck' in token :
            cnt_struck +=1
        if 'caught' in token :
            cnt_caught +=1
            #print(token)
        if  'electrical'in token :
            cnt_electrical += 1
        if 'electrocution' in token :
            cnt_electrical += 1
        if 'electrocuted' in token :
            cnt_electrical +=1
            
    #electrocution, electrical, electrocuted  = > electrocute

    freq_dict = {}
    freq_dict['fire'] = cnt_fire
    freq_dict['fell'] = cnt_fall
    #freq_dict['collapsed'] = cnt_collapse
    freq_dict['crane'] = cnt_crane
    freq_dict['explosion'] = cnt_explosion
    freq_dict['struck'] = cnt_struck
    freq_dict['caught'] = cnt_caught
    freq_dict['electrical'] = cnt_electrical

    return freq_dict

'''
2. Frequency of accident occurence days
'''

def freq_of_day(token_sentence) :
    #frequency of five keywords

    cnt_mon =0 
    cnt_tue =0
    cnt_wed =0 
    cnt_thr = 0
    cnt_fri = 0
    cnt_sat = 0
    cnt_sun = 0

    for token in token_sentence :
        if 'monday' in token :
            cnt_mon +=1
        if 'tuesday' in token :
            cnt_tue +=1
        if 'wednesday' in token :
            cnt_wed +=1
        if 'thursday' in token :
            cnt_thr +=1
        if 'friday' in token :
            cnt_fri +=1
        if 'saturday' in token :
            cnt_sat +=1
        if 'sunday' in token :
            cnt_sun +=1
            
            
    freq_day_dict = {}
    freq_day_dict['Mon'] = cnt_mon
    freq_day_dict['Tue'] = cnt_tue
    freq_day_dict['Wed'] = cnt_wed
    freq_day_dict['Thu'] = cnt_thr
    freq_day_dict['Fri'] = cnt_fri
    freq_day_dict['Sat'] = cnt_sat
    freq_day_dict['Sun'] = cnt_sun

    return freq_day_dict


'''
3. frequency by weather
'''

def generate_by_weather(df_article) :
    weather =[]
    month = []
    years = []
    if "weather" and "month" and "year" in df_article.columns:
        df_article = df_article.drop(["weather","month","year"], axis = 1)
    for i in range(len(df_article)) :

        if df_article.loc[i,'date'] is None :
            weather.append('None')
            month.append('None')
        
            years.append('None')
        else :
            
            year =df_article.loc[i,"date"][:4]
            years.append(year)
                
            if df_article.loc[i,"date"][4:6] == '03':
                weather.append('spring')
                month.append('march')
                
            elif df_article.loc[i,"date"][4:6] == '04' :
                weather.append('spring')
                month.append('april')
                
            elif df_article.loc[i,"date"][4:6] == '05' :
                weather.append('spring')
                month.append('may')
                
            elif df_article.loc[i,"date"][4:6] == "06" :
                weather.append('summer')
                month.append('june')
                
            elif df_article.loc[i,"date"][4:6] == "07" :
                weather.append('summer')
                month.append('july')
                
            elif df_article.loc[i,"date"][4:6] == "08" :
                weather.append('summer')
                month.append('august')
                
            elif df_article.loc[i,"date"][4:6] == "09" :
                weather.append('fall')
                month.append('september')
                
            elif df_article.loc[i,"date"][4:6] == "10" :
                weather.append('fall')
                month.append('october')
                
            elif df_article.loc[i,"date"][4:6] == "11" :
                weather.append('fall')
                month.append('november')
                
            elif df_article.loc[i,"date"][4:6] == "12" :
                weather.append('winter')
                month.append('december')
                
            elif df_article.loc[i,"date"][4:6] == "01" :
                weather.append('winter')
                month.append('january')
                
            elif df_article.loc[i,"date"][4:6] == "02" :
                weather.append('winter')
                month.append('february')
                
            else :
                weather.append('error')
                
    df_article.insert(3, "weather", weather)
    df_article.insert(4, "month", month)
    df_article.insert(5,"year",years)

    return df_article

'''
4. Frequency by year
'''

def get_dist_year(df) :
    
    year_set ={}
    for i in range(len(df)) :
        current = df.loc[i,"year"]
        if current not in year_set :
            year_set[current] = 1
        else : 
            year_set[current] +=1
    
    return year_set

'''
5. Frequency by causation
'''

def get_dist_weather_keyword(df,key) :
    spring_cnt = 0
    summer_cnt =0
    fall_cnt =0
    winter_cnt = 0
    none_cnt = 0
    for i in range(len(df)) :
        if df.loc[i,"weather"] =='spring' :
            #print(type(df.loc[i,"bodies"]))
            if key in df.loc[i,"body"] :
                spring_cnt +=1
        elif df.loc[i,"weather"] =='summer' :
            if key in df.loc[i,"body"] :
                summer_cnt +=1
        elif df.loc[i,"weather"] =='fall' :
            if key in df.loc[i,"body"] :
                fall_cnt +=1
        elif df.loc[i,"weather"] =='winter' :
            if key in df.loc[i,"body"] :
                winter_cnt +=1
        else :
                none_cnt +=0
    
    fin_set_fire = {}
    fin_set_fire['spring'] = spring_cnt
    fin_set_fire['summer'] = summer_cnt
    fin_set_fire['fall'] = fall_cnt
    fin_set_fire['winter'] = winter_cnt
    fin_set_fire['none'] = none_cnt
    
    return fin_set_fire


'''
6. Frequency by month
'''

def get_dist_month(df) :
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
    for i in range(len(df)) :
        if df.loc[i,"month"] =='january' :
            #print(type(df.loc[i,"bodies"]))
       
            jan_cnt +=1
        elif df.loc[i,"month"] =='february' :
        
            feb_cnt +=1
        elif df.loc[i,"month"] =='march' :
        
            mar_cnt +=1
        elif df.loc[i,"month"] =='april' :
   
            apr_cnt +=1
        elif df.loc[i,"month"] =='may' :
     
            may_cnt +=1
        elif df.loc[i,"month"] =='june' :
            
            jun_cnt +=1
        elif df.loc[i,"month"] =='july' :
          
            jul_cnt +=1
        elif df.loc[i,"month"] =='august' :
           
            aug_cnt +=1
        elif df.loc[i,"month"] =='september' :
          
            sep_cnt +=1
        elif df.loc[i,"month"] =='october' :
           
            ocb_cnt +=1
        elif df.loc[i,"month"] =='november' :
            
            nov_cnt +=1
        elif df.loc[i,"month"] =='december' :
            
            dec_cnt +=1
        else :
            none_cnt +=1
    
    fin_set_mon = {}
    fin_set_mon['Jan'] = jan_cnt
    fin_set_mon['Feb'] = feb_cnt
    fin_set_mon['Mar'] = mar_cnt
    fin_set_mon['Apr'] = apr_cnt
    fin_set_mon['May'] = may_cnt
    fin_set_mon['Jun'] = jun_cnt
    fin_set_mon['Jul'] = jul_cnt
    fin_set_mon['Aug'] = aug_cnt
    fin_set_mon['Sep'] = sep_cnt
    fin_set_mon['Oct'] = ocb_cnt
    fin_set_mon['Nov'] = nov_cnt
    fin_set_mon['Dec'] = dec_cnt
    fin_set_mon['none'] = none_cnt
    
    
    return fin_set_mon
    
if __name__ == '__main__' :

    #barchart with label example

    #autolabel

    def autolabel(rects):

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    #frequency histogram of days keywords

    fig, ax = plt.subplots()
    rect = ax.bar(list(freq_day_dict.keys()),freq_day_dict.values(),width = 0.5, color ='gray')
    ax.plot(list(freq_day_dict.keys()),list(freq_day_dict.values()), color = 'red')
    ax.set_ylabel('FREQUENCY', fontsize = 13)
    ax.set_xlabel('DAYS', fontsize =13)
    ax.set_ylim(0,750)

    autolabel(rect)
    #plt.title("Frequency of days")
    fig.tight_layout()
    #plt.savefig('figure/prediction/current/frequency_day.jpeg',dpi=300)