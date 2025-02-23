import os

from flask import Flask, jsonify, redirect, request

import wolframalpha

API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')
DEBUG = os.getenv('DEBUG', False)

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if API_KEY is None:
        return 'Missing configuration for API_KEY', 500

    client = wolframalpha.Client(API_KEY)
    query = request.args.get('query')
    if query is None:
        return jsonify({'text': "API home page"})

    res = client.query(query)
    try:
        response = next(res.results).text
        return jsonify({'text': "OK", 'result': response})
    except StopIteration:
        return jsonify({'text': "Sorry, I couldn't get a result for that query.", 'result': ""})


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if API_KEY is None or TOKEN is None:
            return 'Missing configuration for API_KEY and/or TOKEN', 500
        if request.form['token'] != TOKEN:
            return 'Unauthorized', 401
        # https://docs.python.org/3/library/stdtypes.html#str.split
        query = request.form['text'].split(' ', 1)[1]
        client = wolframalpha.Client(API_KEY)
        res = client.query(query)

        if len(res.pods) == 0:
            return jsonify({'text': "Sorry, I couldn't find any relevant information for you."})
        try:
            response = next(res.results).text
        except StopIteration:
            response = "Sorry, I couldn't get a result for that query."
        return jsonify({'text': response})
    if request.method == 'GET':
        return 'See https://github.com/chdsbd/wolframalpha-bot'


if __name__ == "__main__":
    app.run(debug=DEBUG)
