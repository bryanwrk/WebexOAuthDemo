# -*- coding:utf-8 -*-
import requests
import json


from flask import Flask, render_template, request


app = Flask(__name__)

clientID = "C3ea3bb7e418a783fce06d061fce51e943348bd20a0153b0de0271cef9861be18"
secretID = "55b6b39637d610381e4cada505595ee434f6271807294d21e2c6be791e975ade"
redirectURI = "http://0.0.0.0:10060/oauth" #This could be different if you publicly expose this endpoint.


def get_tokens(code):
    #Gets access token and refresh token
    print "code:", code
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(clientID, secretID, code,  redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    print results
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    return access_token, refresh_token

@app.route("/")

def main_page():
    """Main Grant page"""
    return render_template("index.html")


@app.route("/oauth") #Endpoint acting as Redirect URI.

def oauth():
    """Retrieves oauth code to generate tokens for users"""

    if "code" in request.args and request.args.get("state") == "set_state_here":
        state = request.args.get("state") #Captures value of the state.
        code = request.args.get("code") #Captures value of the code.
        print "OAuth code:", code
        print "OAuth state:", state
        access_token, refresh_token = get_tokens(code) #As you can see, get_tokens() uses the code and returns access and refresh tokens.

        print "Access Token:", access_token
        print "Refresh Token:", refresh_token

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run("0.0.0.0", port=10060, debug=False)
