from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import pandas as pd
import yfinance as yf
from datetime import date, datetime
# "Mon Oct 10 17:23:48 PDT 2016"


# init app
app = Flask(__name__)


def process(symbol):
    stock = yf.Ticker(symbol)
    rslt = ""
    shortN = stock.info['shortName']
    regularMP = stock.info['regularMarketPrice']
    marketPC = stock.info['regularMarketPrice'] - stock.info['previousClose']
    marketPCP = marketPC / stock.info['previousClose'] * 100
    current = datetime.now()
    rslt += current.strftime("%a %b %d %H:%M:%S PDT %Y")
    rslt += f"<br>{shortN} ({symbol})<br>"
    rslt += f"{regularMP} {marketPC:.02f} ({marketPCP:.02f}%)"
    return rslt


@ app.route('/', methods=['GET'])
def get():
    return render_template("index.html")


@app.route('/', methods=["POST"])
def post():
    symbol = request.form["symbol"]
    return redirect(url_for("symbol", sbol=symbol))


@app.route("/finance/<sbol>", methods=["GET"])
def symbol(sbol):
    print('Symbol:', sbol)
    combine = process(sbol)
    result = {
        "output": combine
    }
    return jsonify(result=result)


# run server
if __name__ == '__main__':
    app.run(debug=True)
