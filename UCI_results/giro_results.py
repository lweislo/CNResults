import requests
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def output_file(header_list, table_list):
    outfile = input("Enter your desired CSV filename: " or "giro_results.csv")
    with open(outfile, 'w') as file:
        for item in range(0, len(header_list)):
            file.write(f'\n {header_list[item]}\n')
            file.write(table_list[item].to_csv(header=False, index=False))
def init_browser():
    # Mac-specific browser init
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def format_tables(headers, table_list):
    for item in range(0, len(table_list)):
        if "Tempo" in table_list[item]:
            table_list[item] = table_list[item][["Unnamed: 1", "Corridore","Tempo"]]
            table_list[item]["Tempo"] = table_list[item]["Tempo"].str.replace("h ", ":").str.replace("\’ ",":").str.replace("”", "")
        elif "punti" in table_list[item]:
            table_list[item] = table_list[item][["Unnamed: 1", "Corridore","punti"]]
        elif "Team.1" in table_list[item]:
            table_list[item] = table_list[item][["Unnamed: 1", "Corridore"]]

    for item in table_list:
        item['Corridore'] = item['Corridore'].map(macros).fillna(item['Corridore'])

    header_list = []
    for item in headers:
        header_list.append(item.split("| ")[1].split(" (Ufficiale)")[0])
    output_file(header_list, table_list)

def parse_tables(stage_tables):
    headers = []
    table_list = []
    for n in range(1,3):
        for item in stage_tables[n]:
            try:
                head = item.find('h2').get_text()
                headers.append(head)
                tables = item.find('table')
                table_list.append(pd.read_html(str(tables))[0])
            except ElementDoesNotExist:
                print("No valid results found, sorry")
    format_tables(headers, table_list)

def scrape_giro(stage):
    browser = init_browser()
    browser.visit(stage)
    sleep(5)
    # Scrape the page
    soup = BeautifulSoup(browser.html, 'lxml')
    try:
        stage_tables = soup.find_all('div', class_='tabs-content')
    except ElementDoesNotExist:
        print("Results not found")
    browser.quit()
    parse_tables(stage_tables)

def load_macro():
# find/replace name macro without headers, 2 columns, 1st col= RCS Sport format rider/team, 2nd col=CN format.
    default_macro = "~/Downloads/gironames.csv"
    macro_file = input("Enter location for CSV with find-replace columns:" or default_macro)
    macro = pd.read_csv(macro_file, header=None, index_col=False, names=['name','value'])
    macros = macro.set_index('name').to_dict()['value']
def start():
    load_macro()
    default_url = "http://www.giroditalia.it/it/classifiche/"
    stage = input("Enter the URL" or default_url)
    scrape_giro(stage)
start()
