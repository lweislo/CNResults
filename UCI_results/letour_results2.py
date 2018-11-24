import requests
import html5lib
import pandas as pd
from bs4 import BeautifulSoup


#type_dict = {'e':'Stage', 'g':'General Classification'}
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
start_url = "https://www.tour-de-yorkshire.co.uk/en/rankings/stage-4"
base_url = start_url.split('/')[2]
#Get the html from the page
page = requests.get(start_url)
content = page.content
soup = BeautifulSoup(content, "html5lib")

all_links = soup.find_all(class_="tabs__link js-tabs-ranking")
#grabbing the block of ajax links that give URLs to various stage/GC results
for item in all_links:
    myurl = item['data-ajax-stack']
    #clean up the code into a useable URL
    badchr = ('{', '}', '"')
    for item in badchr:
        myurl = myurl.replace(item, '')
        myurl = myurl.replace('\/', '/')

    myurl = dict(x.split(':') for x in myurl.split(','))
#myurl is now a dictionary with TLA for result type:URL to results (key:value)
    for key, value in myurl.items():
        r_type = tab_dict[key]
        print("Getting the data for: " + r_type)
        url = ("http://" + base_url + value)
        try:
            if key == "ipe" or key == "ime":

                page = requests.get(url).content
                soup = BeautifulSoup(page, "html5lib")
                tables = soup.find(class_="tabs__content")
                for header in tables.find_all(class_="rankingTables__caption"):
                    header = header.text.title()
                #for table in tables.find_all(class_="rankingTable"):
                res_table = pd.read_html(page)
                df = res_table[0]
                print(type(df))

                #heading = soup.find_all('div', class_="rankingTables__caption")
                #for caption in soup.find_all('div', class_="rankingTables__caption"):
                #    res_caption = caption.text.title()
                #    print(res_caption)
                #for rtable in soup.find_all()
                    #res_table = pd.read_html(table)
                    #df = res_table[0]
                    #print(df)
            else:
                page = requests.get(url).content
                soup = BeautifulSoup(page, "html5lib")
                res_table = pd.read_html(page)
                df = res_table[0]
                print(df)

        except ValueError:
            print("No table found for " + key)
            break
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
