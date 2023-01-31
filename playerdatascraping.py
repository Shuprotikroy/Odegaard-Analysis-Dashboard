import requests
from bs4 import BeautifulSoup as soup
import json
import pandas as pd

url ='https://understat.com/player/2517'
html = requests.get(url)
parse_soup = soup(html.content,'lxml')
scripts = parse_soup.find_all('script')
strings = scripts[3].string
ind_start = strings.index("('")+2
ind_end = strings.index("')")
json_data = strings[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)
x = []
y = []
xg = []
result = []
season = []
lastAction=[]
player_assisted=[]
for i,_ in enumerate(data):
    for key in data[i]:
        if key=='X':
            x.append(data[i][key])
        if key=='Y':
            y.append(data[i][key])
        if key=='xG':
            xg.append(data[i][key])
        if key=='result':
            result.append(data[i][key])
        if key=='season':
            season.append(data[i][key])
        if key=='lastAction':
            lastAction.append(data[i][key])
        if key=='player_assisted':
            player_assisted.append(data[i][key])    
columns = ['X','Y','xG','Result','Season','LastAction','player_assisted']
odegaard_data = pd.DataFrame([x, y, xg, result, season,lastAction,player_assisted], index=columns)
odegaard_data = odegaard_data.T
odegaard_data = odegaard_data.apply(pd.to_numeric,errors='ignore')
#scaling to 100 as opta utilises 100x100 pitches
odegaard_data['X'] = odegaard_data['X'].apply(lambda x:x*100)
odegaard_data['Y'] = odegaard_data['Y'].apply(lambda x:x*100)
print(odegaard_data)