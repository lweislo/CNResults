import requests
import html5lib
import pandas as pd
from bs4 import BeautifulSoup
from itertools import chain

type_dict = {'e':'Stage', 'g':'General Classification'}
tab_dict = {'ite':'Stage',
'ipe':'Points',
'ime':'Mountains',
'ije':'Young riders',
'ice':'Combativity',
'ete':'Teams',
'itg':'General Classification',
'ipg':'Points Classification',
'img':'Mountains Classification',
'ijg':'Young Riders Classification',
'icg':'Combativity Classification',
'etg':'Teams Classification'}
#Add a user input for the URL
start_url = "https://www.letour.fr/en/rankings/stage-19"
base_url = start_url.split('/')[2]

page = requests.get(start_url)
content = page.content
r_table = pd.read_html(content)

#This worked to get the table out into a DataFrame
df = r_table[0]
#print(df['Rider'])

soup = BeautifulSoup(content, "html5lib")

#results = soup.find_all(class_="rankingTabs__content")
#print(results)
#links = soup.find_all(class_="tabs__link js-tabs-ranking-nested stage")
all_links = soup.find_all(class_="tabs__link js-tabs-ranking")

link_dict = {}
count = 0
for item in all_links:
    myurls = item['data-ajax-stack']
    #The ajax stack is formatted with escape characters and double quotes, remove those
    #then turn the ajax list into a python dictionary
    badchr = ('{', '}', '"')
    for item in badchr:
        myurls = myurls.replace(item, '')
        myurls = myurls.replace('\/', '/')
    link_dict = dict(x.split(':') for x in myurls.split(','))
#Now we have to go through and change the keys to full names for classifications

for key, value in link_dict.items():
    link_dict[key] = ("http://" + base_url + link_dict[key])






#Need to figure out how to deal with the URLs from this dictionary

#stage_links = []
#stage_type = []
#for item in links:
#    result_type = (tab_dict[item['data-type'][0:2]] + ' ' + type_dict[item['data-type'][-1]])
#    url = 'https://' + base_url + item['data-tabs-ajax']
#    stage_links.append(url)
#    stage_type.append(result_type)
    #print(url)
#for link in stage_links:
#    page = requests.get(link)
#    content = page.content
#    result_table = pd.read_html(content)
    #print(result_table)
