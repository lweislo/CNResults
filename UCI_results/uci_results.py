import pandas as pd
import os
import glob

def cn_format(df1, file_name):

    try:
#Reformat the dataframe
#Taking DNF/DNS from IRM column and adding to blank values in Rank
        df1['Rank'] = df1['Rank'].fillna(df1['IRM'])
#Combining First and non-UPPER last names
        df1['Name'] = (df1['First Name'] + ' ' + df1['Last Name'].str.title())
#Getting rid of non-time values in Result column.
        df1.loc[:,'Result'] = df1['Result'].where((df1['Result'].astype(str).str.contains(':') == True), df1['Result'].astype(str).str[''])
#mapping the UCI country codes to CN code dictionary
        df1['Country'] = df1['Country'].map(countries_short_dict).fillna("(" + df1['Country'].str.title() + ")")
#Reformat teams
        df1['Team'] = df1['Team'].fillna('').str.title()
#finally format rider/country/team
        df1['Rider'] = (df1['Name'] + ' ' + df1['Country'] + ' ' + df1['Team'])
#Now output the three important columns to Excel
        writer = pd.ExcelWriter('output(' + file_name + ').xlsx')
        df1.to_excel(writer, "Sheet1", startrow=0, header=False, index= False, columns=['Rank', 'Rider', 'Result'] )
#CN macros need three sheets
        workbook  = writer.book
        worksheet = workbook.add_worksheet()
        worksheet = workbook.add_worksheet()
        writer.save()
    except:
        print(f"Error running the file {file_name}")

countries_short_dict = {"ALB": "(Alb)", "ALG": "(Alg)", "AND": "(And)", "ANG": "(Ang)", "ANT": "(Ant)", "ARG": "(Arg)", "ARM": "(Arm)", "ARU": "(Aru)", "AUS": "(Aus)", "AUT": "(Aut)", "AZE": "(Aze)", "BAH": "(Bah)", "BRN": "(Brn)", "BAN": "(Ban)", "BAR": "(Bar)", "BLR": "(Blr)", "BEL": "(Bel)", "BIZ": "(Biz)", "BEN": "(Ben)", "BER": "(Ber)", "BOL": "(Bol)", "BIH": "(BiH)", "BRA": "(Bra)", "BRU": "(Bru)", "BUL": "(Bul)", "BUR": "(Bur)", "BDI": "(Bdi)", "CMR": "(Cmr)", "CAN": "(Can)", "CPV": "(CpV)", "CAY": "(Cay)", "CHI": "(Chi)", "CHN": "(Chn)", "TPE": "(Tpe)", "COL": "(Col)", "COM": "(Com)", "CRC": "(CRc)", "CRO": "(Cro)", "CUB": "(Cub)", "CYP": "(Cyp)", "CZE": "(Cze)", "DEN": "(Den)", "DOM": "(Dom)", "ECU": "(Ecu)", "EGY": "(Egy)", "ESA": "(ESa)", "ERI": "(Eri)", "EST": "(Est)", "ETH": "(Eth)", "FIJ": "(Fij)", "FIN": "(Fin)", "FRA": "(Fra)", "GAB": "(Gab)", "GEO": "(Geo)", "GER": "(Ger)", "GRE": "(Gre)", "GRN": "(Grn)", "GUM": "(Gum)", "GUA": "(Gua)", "GUI": "(Gui)", "GUY": "(Guy)", "HAI": "(Hai)", "HON": "(Hon)", "HKG": "(HKg)", "HUN": "(Hun)", "ISL": "(Isl)", "IND": "(Ind)", "INA": "(Ina)", "IRI": "(IRI)", "IRQ": "(Irq)", "ISR": "(Isr)", "ITA": "(Ita)", "CIV": "(CIv)", "JAM": "(Jam)", "JPN": "(Jpn)", "JOR": "(Jor)", "KAZ": "(Kaz)", "KEN": "(Ken)", "KOS": "(Kos)", "KUW": "(Kuw)", "KGZ": "(Kgz)", "Laos": "Laos", "LAT": "(Lat)", "LIB": "(Lib)", "LES": "(Les)", "LIE": "(Lie)", "LTU": "(Ltu)", "LUX": "(Lux)", "MAC": "(Mac)", "MKD": "(Mkd)", "MAD": "(Mad)", "MLI": "(Mli)", "MAS": "(Mas)", "MLT": "(Mlt)", "MRI": "(Mri)", "MEX": "(Mex)", "MDA": "(Mda)", "MON": "(Mon)", "MGL": "(Mgl)", "MNE": "(Mne)", "MAR": "(Mar)", "MYA": "(Mya)", "NAM": "(Nam)", "NEP": "(Nep)", "NED": "(Ned)", "AHO": "(AHo)", "NZL": "(NZl)", "NCA": "(Nca)", "NIG": "(Nig)", "NGR": "(Ngr)", "PRK": "(PRK)", "NOR": "(Nor)", "OMA": "(Oma)", "PAK": "(Pak)", "PAN": "(Pan)", "PAR": "(Par)", "PER": "(Per)", "PHI": "(Phi)", "POL": "(Pol)", "POR": "(Por)", "PUR": "(PuR)", "QAT": "(Qat)", "IRL": "(Irl)", "CGO": "(Cgo)", "ROU": "(Rom)", "RUS": "(Rus)", "RWA": "(Rwa)", "SKN": "(SKN)", "LCA": "(Lca)", "VIN": "(Vin)", "SMR": "(SMr)", "KSA": "(KSA)", "SEN": "(Sen)", "SRB": "(Srb)", "SEY": "(Sey)", "SIN": "(Sin)", "SVK": "(Svk)", "SLO": "(Slo)", "SOM": "(Som)", "RSA": "(RSA)", "KOR": "(Kor)", "ESP": "(Spa)", "SRI": "(Sri)", "SUD": "(Sud)", "SUR": "(Sur)", "SWE": "(Swe)", "SUI": "(Swi)", "SYR": "(Syr)", "TJK": "(Tjk)", "THA": "(Tha)", "TOG": "(Tog)", "TRI": "(Tri)", "TUN": "(Tun)", "TUR": "(Tur)", "TKM": "(Tkm)", "UGA": "(Uga)", "UKR": "(Ukr)", "UAE": "(UAE)", "GBR": "(GBr)", "USA": "(USA)", "URU": "(Uru)", "UZB": "(Uzb)", "VEN": "(Ven)", "VIE": "(Vie)", "YEM": "(Yem)", "ZAM": "(Zam)", "ZIM": "(Zim)"}

# Change directory
results_loc = "/Users/lauraweislo/Downloads/"#input("Enter the path for your download directory: ")
os.chdir(results_loc)

# List all files and directories in current directory
files = glob.glob((results_loc + "/*.xlsx").split("/")[-1])

# Loop through each spreadsheet and create a dataframe

for item in files:
    file_count = 0
    if "Results" in item:
        xl = pd.ExcelFile(item)
# Get the portion of the filename
        if '(' in item:
            file_name = item.replace('Results (', '').replace(')', '').replace('.xlsx', '')
        else:
            file_name = str(file_count)
        #print(file_name)
        file_count += 1
# Load a sheet into a DataFrame by name: df1
        df1 = xl.parse('Results')
        cn_format(df1, file_name)
