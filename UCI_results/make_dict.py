import pandas as pd
import os
import json
#results_loc = input("Enter the path for your download directory: ")

def make_country_dict():
    xl_file = input('Enter the file with full path (/Users/././..xlsx :')
    #read in the file
    source_file = pd.ExcelFile(xl_file)
    #bring in the sheets as dataframes
    df_short = pd.read_excel(source_file, 'short')
    df_long = pd.read_excel(source_file, 'long')
    df_long_short = pd.read_excel(source_file, 'long_to_short')
    #convert the dataframes to dictionaries
    countries_short_dict = df_short.set_index('UCI_code').to_dict()['CN_short']
    countries_long_dict = df_long.set_index('UCI_code').to_dict()['CN_long']
    long_to_short_dict = df_long_short.set_index('Name').to_dict()['CN_short']

    #create the dictionary files
    with open('country_dict.py', 'w') as f:
        json.dump(countries_short_dict, f)
        json.dump(countries_long_dict, f)
        json.dump(long_to_short_dict, f)

    print("done")

def make_other_dict(choice):
    #read in the file
    source_file = pd.ExcelFile(choice)
    outfile = 'my_test.py'
    #bring in the sheets as dataframes
    df = pd.read_excel(source_file, 'Sheet1')

    new_dict = df.set_index('Bib').to_dict()['Name']

    with open(f'{outfile}','w+') as f:
        json.dump(new_dict, f)
    #print(new_dict)

choice = input("Enter the full path of your xl file: ")
make_other_dict(choice)
