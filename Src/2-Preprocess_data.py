import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import pickle

class ArticleInfo():
    
    def __init__(self, s_url) :
        
        session = requests.Session()
        req=session.get(s_url)
        self.soup = BeautifulSoup(req.text, 'html.parser')
    
    
    def article_body(self) :
        body = self.soup.find('div', {'class' : 'StoryBodyCompanionColumn'})
        finalContent =''
    
        if body is not None :
            for itcontents in self.soup.findAll('p'):
                if itcontents == None :
                    continue
                content = itcontents.getText()
                content = re.sub(r"\n+", "", content)
                finalContent +=content
        else :
            return False
        
        return finalContent

    def article_title(self):
        titles = self.soup.select('title',{"data-rh":"true"})
        for title in titles:
            title = title.getText()
            break
        return title

    def article_date(self) :
  
        date = self.soup.find('li',{'class':'date'})
        if date != None :
            date = date.getText()
            
        else :
            date = self.soup.find('meta',{'name':'pdate'})
            if date !=None :
                date = date.get('content')
                if date !=None :
                    date = str(date)
                else:
                    none= "none"
                    datelist.append(none)
                
        return date

def scraping(source_link):
    titles =[]
    bodies =[]
    datelist=[]

    for s_url in source_link :
        s_url = 'https://www.nytimes.com'+s_url
        ob = ArticleInfo(s_url)

        body =ob.article_body()
        bodies.append(body)

        date = ob.article_date()
        datelist.append(date)

        title = ob.article_title()
        titles.append(title)
    return bodies, datelist, titles


if __name__ == '__main__' :

    #repeat this depends on sliced data -> here, a,b,c,d,e,f
    body, date, title = scraping(new_f)

    date_list = [a_date,b_date,c_date,d_date,e_date,f_date]
    body_list = [a_body,b_body,c_body,d_body,e_body,f_body]
    title_list = [a_title,b_title,c_title,d_title,e_title,f_title]
    final_set = {}
    final_set['date'] = []
    final_set['title'] = []
    final_set['body'] = []
    for i in range(len(date_list)) :
        
        final_set['date'].extend(date_list[i])
        final_set['title'].extend(title_list[i])
        final_set['body'].extend(body_list[i])
        
    df_nyt = pd.DataFrame(final_set, columns =["date", "title", "body"])
    df_nyt.to_pickle("./nyt_df.pkl")