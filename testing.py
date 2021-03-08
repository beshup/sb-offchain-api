from bs4.element import ResultSet
from nba_api.stats.static import players, teams
import requests
import json
from bs4 import BeautifulSoup
"""
# SCRIPT TO GET PICS OF THE PLAYERS

url = "https://basketball.realgm.com/nba/players" 
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
job_elems = soup.find_all('tr')
data = []
for job_elem in job_elems:
    name = job_elem.find_all('a', href = True)
    pos = job_elem.find('td', attrs = {'data-th' : "Pos"})
    try:
        acc_name = name[0]
        acc_team = name[1]
        url = acc_name['href']
        name_page = requests.get("https://basketball.realgm.com/"+url)
        soup_2 = BeautifulSoup(name_page.content, 'html.parser')
        pic = soup_2.find('img', src = True, style = "border: 1px solid #000; float: left; margin-right: 15px; margin-top:5px;")
        data.append({
            'name': acc_name.text,
            'pic':"https://basketball.realgm.com"+pic['src']
        })
    except Exception as e: 
        print(e)
        continue

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

#UNTIL HERE

#SCRIPT TO GET FANTASY DATA FOR THE PLAYERS (TOP 50)

url = "https://hashtagbasketball.com/fantasy-basketball-points-league-rankings" 
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
job_elems = soup.find_all('tr')
data = []
for job_elem in job_elems:
    values = job_elem.find_all('span')
    #print(values)
    try:
        rank = values[0]
        name = values[1]
        fantasy_pts = values[2]
        position = values[3]
        team = values[4]
        if int(rank.text) < 51:
            data.append({
                'name': name.text,
                'position': position.text,
                'team': team.text,
                'fantasy_points': fantasy_pts.text,
                'fantasy_rank': rank.text
            })
    except Exception as e: 
        #print(e)
        continue

with open('fantasy_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
"""
#UNTIL HERE
    

main_file = open('fantasy_data.json', 'r')
pic_file = open('data.json', 'r')

main_data = json.load(main_file)
pic_data = json.load(pic_file)

new = []
for element in main_data:
    name = element["name"]
    for elem in pic_data:
        if name == elem["name"]:
            new.append({
                'name': name,
                'position': element['position'],
                'team': element['team'],
                'fantasy_points': element['fantasy_points'],
                'pic': elem['pic'],
                'token_id': element['fantasy_rank']
            })
with open('new_file.json', 'w', encoding='utf-8') as f:
    json.dump(new, f, ensure_ascii=False, indent=4)
 