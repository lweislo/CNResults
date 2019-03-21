import requests
import html5lib
import pandas as pd
from bs4 import BeautifulSoup
import os

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

order_list = ['ite', 'ipe', 'ime', 'ije', 'ice', 'ete', 'itg', 'ipg', 'img', 'ijg', 'etg', 'icg']
points_stg = ['ipe', 'ime']
out_df = pd.DataFrame()

def output_res(df, label):

    with open(f'{outfile}','a+') as output:
        output.write(label + '\n')
        df.to_csv(output, header=False, sep = "\t", index_label=False)

def get_urls(all_links):
    url_dict = {}

    for item in all_links[::-1]:
        myurl = item['data-ajax-stack']
        #clean up the code into a useable URL
        badchr = ('{', '}', '"')
        for item in badchr:
            myurl = myurl.replace(item, '')
            myurl = myurl.replace('\/', '/')
        myurl = dict(x.split(':') for x in myurl.split(','))
        myurl = {k:f'http://{base_url}{v}' for (k,v) in myurl.items()}
        for key, value in myurl.items():
            url_dict[key] = value

    get_results(url_dict)
#myurl is now a dictionary with TLA for result type:URL to results (key:value)

def get_results(url_dict):
    count = 0
    label = ''

    #for l_item in order_list:
    for l_item in order_list:
        url = url_dict[l_item]
        r_type = tab_dict[l_item]
        print("Getting the data for: " + r_type)

        try:
    #Treat sprint and mountains stage results differently
    #They have multiple tables per page
            if l_item != 'ipe' or l_item != 'ime':
                page = requests.get(url).content
                soup = BeautifulSoup(page, "html5lib")
                res_table = pd.read_html(page)
                df = res_table[0]
                label = r_type

                if l_item in ['ite', 'ije', 'itg', 'ijg']:
                    out_df['Place'] = df['Rank'].fillna('')
                    out_df['Bib'] = df['Rider No.'].fillna('')
                    out_df['Result'] = df['Times'].str.replace('h ', ':').str.replace('\'\'', '').str.replace('\' ',':')
                elif l_item in ['ipg', 'img']:
                    out_df['Place'] = df['Rank'].fillna('')
                    out_df['Bib'] = df['Rider No.'].fillna('')
                    out_df['Result'] = df['Points'].str.replace(' PTS', '')
                elif l_item == 'ice':
                    out_df['Place'] = df['Rank'].fillna('')
                    out_df['Bib'] = df['Rider No.'].fillna('')
                    out_df['Result'] = ''
                elif l_item in ['ete', 'etg']:
                    out_df['Place'] = df['Rank'].fillna('')
                    out_df['Bib'] = df['Team'].str.title().fillna('')
                    out_df['Result'] = df['Times'].str.replace('h ', ':').str.replace('\'\'', '').str.replace('\' ',':')
#Augh, now the goddamn output has the same number of rows for every set.
                #out_df = df[df.columns[-3:]]
                output_res(out_df, label)

            else:
                page = requests.get(url).content
                soup = BeautifulSoup(page, "html5lib")
                tables = soup.find(class_="tabs__content")
                for item in tables.find_all(class_="rankingTables__caption"):
                    count +=1
                    label = (r_type + ' ' + str(count) + ' - ')
                    header = item.text.title()
        #Using the page content, grab the tables.
                    res_table = pd.read_html(page)
                    df = res_table[0]
                    out_df['Place'] = df['Rank'].fillna('')
                    out_df['Bib'] = df['Team'].fillna('')
                    out_df['Result'] = df['Points'].str.replace('PTS', '')
                    #out_df = df[df.columns[-3:]]
                    label = (header + label)
                    output_res(out_df, label)
                    label = ''

        except ValueError:
            print("No table found for " + r_type)

def start():
    #Get the html from the page
    page = requests.get(start_url)
    content = page.content
    soup = BeautifulSoup(content, "html5lib")
    #Pull out a specific block of code with two sets of coded URLs.
    all_links = soup.find_all(class_="tabs__link js-tabs-ranking")

    if len(all_links) == 0:
        print("That doesn't appear to be an ASO results page as we know it.")
    else:
        get_urls(all_links)

try:
    start_url = 'https://www.paris-nice.fr/en/rankings/stage-2' #input("Enter the results URL: ")
    base_url = start_url.split('/')[2]
    outfile = (start_url.split('www.')[1].split('.')[0] + '_'+ start_url.split('/')[-1] + '.csv')

except:
    print("That does not appear to be a valid results URL.")

start()
