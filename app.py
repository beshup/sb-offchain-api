from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS, cross_origin
import requests
import json
import copy 
app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#TODO: add onto API to hold top performers of each week, but each static week, not in the past week


# ===================================================================================================================================================================
# ===================================================================================================================================================================
# CONSTANTS
# ===================================================================================================================================================================
# ===================================================================================================================================================================


LEAGUE_SIZE = 50 


# ===================================================================================================================================================================
# ===================================================================================================================================================================
# ENDPOINTS  
# ===================================================================================================================================================================
# ===================================================================================================================================================================


@app.route('/to_send_per_entity/<int:entity_id>/<int:shares_owned>/<int:shares_in_circulation>/<int:dividend_fund>', methods=['GET'])
@cross_origin()
def to_send(entity_id, shares_owned, shares_in_circulation, dividend_fund):
    if entity_id > LEAGUE_SIZE:
        entity_id -= LEAGUE_SIZE

    entity_name = league_data()[entity_id - 1]['name']
    fantasy_table = returnFantasyTable()

    #technically not of past week, gotta change
    rows = list(fantasy_table.children)
    sum_scores = 0.0
    res = 0
    row_counter=0
    for row in rows:
        if row != rows[0] and row_counter < 11:
            sum_scores += float(list(row.children)[3].get_text())
        row_counter += 1

    for row in rows:
        if row != rows[0]:
            if entity_name == list(list(row.children)[1])[0].get_text():
                entity_score_share = float(list(row.children)[3].get_text()) / sum_scores
                res = (shares_owned/shares_in_circulation)*entity_score_share*dividend_fund
                break
           
    return {"to_send": int(res)}


@app.route('/grip_league', methods=['GET'])
@cross_origin()
def grip_league():
    return jsonify(league_data())

@app.route('/grip_league_all_types', methods=['GET'])
@cross_origin()
def grip_league_all_types():
    data = league_data()
    nfts = []

    for player in data:
        nft_vzn = copy.deepcopy(player)
        nft_vzn['name'] = player['name'] + " - 2020/2021 Champion"
        nft_vzn['token_id'] = int(player['token_id']) + LEAGUE_SIZE
        nfts.append(nft_vzn)

    return jsonify(data + nfts)    


@app.route('/grip_player/<int:entity_id>', methods=['GET'])
@cross_origin()
def grip_player(entity_id):
    return grip_entity_helper(entity_id)


@app.route('/player_sft_metadata/<int:entity_id>', methods=['GET'])
@cross_origin()
def player_sft_metadata(entity_id):
    player = grip_entity_helper(entity_id)
    del player['fantasy_points']
    return player


# ===================================================================================================================================================================
# ===================================================================================================================================================================
# HELPERS
# ===================================================================================================================================================================
# ===================================================================================================================================================================


def returnFantasyTable():
    url="https://basketballmonster.com/"

    html_content = requests.get(url).content
    page = BeautifulSoup(html_content, "html.parser")

    return page.find("table", attrs={"class": "datatable"})


def returnPlayerScores():
    fantasy_table = returnFantasyTable()
    rows = list(fantasy_table.children)
    player_scores = []

    for row in rows:
        if row != rows[0]:
            player_scores.append(float(list(row.children)[3].get_text()))

    return player_scores        

def grip_entity_helper(entity_id):
    if entity_id <= LEAGUE_SIZE:
        return league_data()[entity_id - 1]
    else:
        sft_counterpart = league_data()[entity_id - LEAGUE_SIZE - 1] 
        sft_counterpart['token_id'] = entity_id 
        return sft_counterpart 

def league_data():
    f = open('new_file.json')
    return json.load(f)['league']


# ===================================================================================================================================================================
# ===================================================================================================================================================================
# SERVER
# ===================================================================================================================================================================
# ===================================================================================================================================================================


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)