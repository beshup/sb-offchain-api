from flask import Flask
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)


@app.route('/nbatoppastweek')
def data():
    res = []
    url="https://basketballmonster.com/"

    html_content = requests.get(url).content
    page = BeautifulSoup(html_content, "html.parser")

    fantasy_table = page.find("table", attrs={"class": "datatable"})
    # technically not of past week, gotta change
    rows = list(fantasy_table.children)
    for row in rows:
        if row != rows[0]:
            res.append({"name": list(list(row.children)[1])[0].get_text(), "score": list(row.children)[3].get_text()})
    
    return res

if __name__ == '__main__':
    app.run()