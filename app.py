from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS, cross_origin
import requests
app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#TODO: add onto API to hold top performers of each week, but each static week

# in db in future LOLs centralized for now
hardchoded_dictionary_for_now = {
    1: "Nikola Jokic",
    2: "Karl-Anthony Towns",
    3: "Joel Embiid",
    4: "Kawhi Leonard",
    5: "Kevin Durant",
    6: "Stephen Curry",
    7: "C.J. McCollum",
    8: "Damian Lillard",
    9: "Kyrie Irving",
    10: "James Harden"
}


@app.route('/to_send_per_entity/<int:entity_id>/<int:shares_owned>/<int:shares_in_circulation>/<int:dividend_fund>', methods=['GET'])
@cross_origin()
def to_send(entity_id, shares_owned, shares_in_circulation, dividend_fund):
    entity_name = hardchoded_dictionary_for_now[entity_id]
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
           
    
    return {"to_send": res}


@app.route('/grip_league', methods=['GET'])
@cross_origin()
def grip_league():
    return jsonify(hardchoded_league(returnPlayerScores()))


@app.route('/grip_player/<int:entity_id>', methods=['GET'])
@cross_origin()
def grip_player(entity_id):
    return hardchoded_league(returnPlayerScores())[entity_id]  


@app.route('/player_sft_metadata/<int:token_id>', methods=['GET'])
@cross_origin()
def player_sft_metadata(token_id):
    player_data = hardchoded_league(returnPlayerScores())[token_id]
    return {"name": player_data["name"], "team": player_data["team"], "token_id": player_data["token_id"], "image": player_data["image"]}


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


# lol harcoded cuz we work and we have no time to do things
def hardchoded_league(player_scores):
    return [
        {"name": "Nikola Jokic", "team": "Denver Nuggets", "position": "C", "fantasy_score": player_scores[0], "token_id": 0, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png"},
        {"name": "Karl-Anthony Towns", "team": "Minnesota Timberwolves", "position": "C", "fantasy_score": player_scores[1], "token_id": 1, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/1626157.png"},
        {"name": "Joel Embiid", "team": "Philadelphia 76ers", "position": "C", "fantasy_score": player_scores[2], "token_id": 2, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png"},
        {"name": "Kawhi Leonard", "team": "Los Angeles Clippers", "position": "F", "fantasy_score": player_scores[3], "token_id": 3, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/202695.png"},
        {"name": "Kevin Durant", "team": "Brooklyn Nets", "position": "F", "fantasy_score": player_scores[4], "token_id": 4, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png"},
        {"name": "Stephen Curry", "team": "Golden State Warriors", "position": "G", "fantasy_score": player_scores[5], "token_id": 5, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png"},
        {"name": "C.J. McCollum", "team": "Portland Trailblazers", "position": "G", "fantasy_score": player_scores[6], "token_id": 6, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/203468.png"},
        {"name": "Damian Lillard", "team": "Portland Trailblazers", "position": "G", "fantasy_score": player_scores[7], "token_id": 7, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/203081.png"},
        {"name": "Kyrie Irving", "team": "Brooklyn Nets", "position": "G", "fantasy_score": player_scores[8], "token_id": 8, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/202681.png"},
        {"name": "James Harden", "team": "Brooklyn Nets", "position": "G", "fantasy_score": player_scores[9], "token_id": 9, "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/201935.png"},
    ]

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)