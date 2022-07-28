from flask import Flask, render_template, request
import os
import json
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    server_data = cloud_info()

    return render_template('index.html', title="Entecraft", server_url=os.getenv("SERVER_URL"), server_data=server_data)


# Internal
@app.route('/cloud/start')
def cloud_start():
    if request.headers['start-server-password'] != os.getenv("START_PASSWORD"):
        return f"Invalid password", 403

    url = "https://s3c06us69j.execute-api.us-west-1.amazonaws.com/default/status?newStatus=ON"

    payload = {}
    headers = {
        'x-api-key': os.getenv("CLOUD_API_KEY")
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    if response.ok:
        return json.dumps("OK. Starting server.")
    else:
        return json.dumps("Something went wrong."), 500


@app.route('/cloud/info')
def cloud_info():
    url = "https://s3c06us69j.execute-api.us-west-1.amazonaws.com/default/status"

    payload = {}
    headers = {
        'x-api-key': os.getenv("CLOUD_API_KEY")
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    return json.loads(response.text)


if __name__ == '__main__':
    app.run(debug=True, port=33507)
