import os
import time
import json
import hashlib
import dataclasses
import logging
import typing
import requests
import flask

from flask import render_template, request, redirect

app = flask.Flask(__name__)


@dataclasses.dataclass
class Rate:
    currency: str
    code: str
    bid: float
    ask: float


class ApiClient:

    def __init__(self, url: str, invalidation_time_in_seconds: int):
        self.url = url
        self.invalidation_time_in_seconds = invalidation_time_in_seconds

    @property
    def data(self):
        bare_data = self._collect_data()
        data = self._read_data(bare_data)
        return data

    def _read_data(self, bare_data):
        return bare_data

    def _collect_data(self) -> dict:
        file_name = hashlib.md5(self.url.encode()).hexdigest() + ".json"
        if os.path.isfile(file_name):
            if time.time() < os.stat(file_name).st_mtime + self.invalidation_time_in_seconds:
                with open(file_name, 'r') as data_file:
                    return json.load(data_file)
        logging.debug("Start communication with API")
        with requests.get(self.url) as response:
            response_data = response.json()
            if isinstance(response_data, list) and response_data:
                data = response_data[0]
                with open(file_name, 'w') as data_file:
                    json.dump(data, data_file)
                return data
        return {}


class NBPApiClient(ApiClient):

    def _read_data(self, bare_data) -> typing.Dict[str, Rate]:
        data_rates = bare_data.get('rates')
        data_rates_normalized = [Rate(**entry) for entry in data_rates]
        return {rate.code: rate for rate in data_rates_normalized}


@app.route("/", methods=['GET'])
def calculator():
    return render_template("currency_calculator.html")


@app.route("/", methods=['POST'])
def insert():
    user_data = request.form
    return redirect('/')


@app.route("/result", methods=['GET'])
def result():
    return render_template('result.html')


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    api_client = NBPApiClient(url="http://api.nbp.pl/api/exchangerates/tables/C?format=json",
                              invalidation_time_in_seconds=600)
    app.run()
