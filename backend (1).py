from flask import Flask, jsonify
from flask_cors import CORS
import random
import numpy as np
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from valag import *
from framvirkir_vextir import *
import datetime
from cs import *
from nss2 import * 

app = Flask(__name__)
CORS(app)

def is_market_open():
    current_time = datetime.datetime.now().time()
    market_close_time = datetime.time(16, 0)  # 16:00 hours

    return current_time < market_close_time

# def credit_spread():
#     """
#         Herna kemur credit spread, sem returnar nafni, krofu a RIK, krofu a brefid, og credit spread
#     """
#     return ["ARION CB", 2, 3, 1]


def framvirkir_vextir():
    return [[1,2], [2,3], [4,5], [7, 8], [10, 9]]

# Define a route to get the line chart data
@app.route('/data')
def data():
    data = nss_main()
    # data = {
    #     'RIKS': [random.randint(0, 100) for _ in range(10)],
    #     'RIKB': [random.randint(0, 100) for _ in range(10)],
    #     'ISB CB': [random.randint(0, 100) for _ in range(10)], #Spurning að beila á þetta
    #     'ISB CBI': [random.randint(0, 100) for _ in range(10)],
    #     'ARION CB': [random.randint(0, 100) for _ in range(10)],
    #     'ARION CBI': [random.randint(0, 100) for _ in range(10)],
    #     'LBANK CB': [random.randint(0, 100) for _ in range(10)],
    #     'LBANK CBI': [random.randint(0, 100) for _ in range(10)],
    #     'RVK': [random.randint(0, 100) for _ in range(10)],
    #     'RVKV': [random.randint(0, 100) for _ in range(10)],
    #     'OR': [random.randint(0, 100) for _ in range(10)],
    #     'LSS': [random.randint(0, 100) for _ in range(10)],
    #     'REGINN': [random.randint(0, 100) for _ in range(10)]
    # }
    return jsonify(data)

@app.route('/table_data')
def table_data():
    table_data = []
    info = credit_spread()
    for i in range(len(info)):
        data = {
            'Name': str(round(info[i][2], 4))+"%",
            'RIK': str(round(info[i][3], 4))+"%",
            'Bond': info[i][0],
            'Credit Spread': str(round(info[i][1], 4))+"%"
        }
        table_data.append(data)
    return jsonify(table_data)


@app.route('/verdbolgualag')
def verdbolga():
    hnit, hnit2 = verdlag()  # Assuming verdlag() returns the desired lists
    return jsonify({'hnit': hnit, 'hnit2': hnit2})

@app.route('/forward_rate')
def forward_rate_route():
    overd = forward_rate()
    return jsonify(overd)

@app.route('/forward_rate_verdtryggt')
def forward_rate_verdtryggt_route():
    verd = forward_rate_verdtryggt()
    return jsonify(verd)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)