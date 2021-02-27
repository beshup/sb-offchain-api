from bs4.element import ResultSet
from nba_api.stats.static import players, teams
import requests
import json
from bs4 import BeautifulSoup
"""
all_players = players.get_players()
c = 0
create_dict = {}

for rec in all_players:
    #print(rec['full_name'])
    if (rec['is_active'] == True):
        c += 1
        create_dict[c] = rec['full_name']

all_teams = teams.get_teams()


url = "https://www.nba.com/players" 
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
#results = soup.find(id='players-list')
job_elems = soup.find_all('div', class_= 'flex flex-col lg:flex-row')

for job_elem in job_elems:
    first = job_elem.find('p', class_= "t6 mr-1")
    last = job_elem.find('p', class_= "t6")
    print(job_elem, end='\n'*2)

    """

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

"""

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