
from selenium import webdriver
import time
from bs4 import BeautifulSoup


# url list from search term "Construction Accident"

'''
m_url ="https://www.nytimes.com/search?dropmab=false&endDate=20191231&query=%22construction%22%20accident&sort=newest&startDate=20000101"
m_url ="https://www.nytimes.com/search?dropmab=false&endDate=20140702&query=%22construction%22%20accident&sort=newest&startDate=20000101"
m_url = "https://www.nytimes.com/search?dropmab=false&endDate=20100207&query=%22construction%22%20accident&sort=newest&startDate=20000101"
m_url = "https://www.nytimes.com/search?dropmab=false&endDate=20070626&query=%22construction%22%20accident&sort=newest&startDate=20000101"
m_url = "https://www.nytimes.com/search?dropmab=false&endDate=20040524&query=%22construction%22%20accident&sort=newest&startDate=20000101"
m_url ="https://www.nytimes.com/search?dropmab=false&endDate=20000605&query=%22construction%22%20accident&sort=newest&startDate=20000101"
'''

if __name__ == '__main__' :

    chrome_options = webdriver.ChromeOptions
    #chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path='/Users/macbookpro/Project_construction/chromedriver')

    link = []
    driver.get(m_url)
    time.sleep(3)
    for i in range(110) :
        a = driver.page_source
        b = BeautifulSoup(a, 'html.parser')
        #stream-panel > div.css-13mho3u > ol > li:nth-child(1) > div > div.css-1l4spti > a
        #stream-panel > div.css-13mho3u > ol > li > div > div.css-1l4spti > a
        #site-content > div > div:nth-child(2) > div.css-46b038 > ol > li:nth-child(1) > div > div > div > a
        c = b.select('#site-content > div >div>div> ol >li> div > div > div > a')
        
        for j in range(len(c)) :
            if c[j].attrs['href'] not in link :
                link.append(c[j].attrs['href'])
            else :
                pass
        
        driver.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button').click()
        time.sleep(3)
