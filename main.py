from flask import Flask, render_template, request, redirect, url_for
from urllib.request import Request, urlopen
import ast, requests
import os, json
import flask_discord
from mongomethods import reading
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)





@app.route("/login/")
def login():
    return redirect('https://discord.com/api/oauth2/authorize?client_id=810662403217948672&redirect_uri=https%3A%2F%2Fcbotdiscord.npcool.repl.co&response_type=code&scope=identify')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404





	


def exchange_code(code):
      data = {
        'client_id': 829032196852940820 ,
        'client_secret': "L9BoTFMp0xOOqNkanjDco6LsWq1UKBFi",
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "https://cbotdiscord.npcool.repl.co"
      }
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
      r = requests.post('https://discord.com/api/v8/oauth2/token', data=data, headers=headers)
      #r.raise_for_status()
      return r.json()
global baseUrl
baseUrl = "https://discordapp.com/api"
def getHeaders(access_token):
    return {
        "Authorization" : "{} {}".format("Bearer", access_token),
        # "user-agent" : "DiscordBackup/0.0.1"
    } 

def getRequest(access_token, endpoint, asJson = True, additional = None):
    url = "{}/{}".format(baseUrl, endpoint)
    req = requests.get(url, headers = getHeaders(access_token))
   
    if asJson:
        return json.loads(req.text)
    else:
        return req.text

def getMe(access_token): # this works
    endpoint = "users/@me"
    return getRequest(access_token, endpoint)


@app.route('/')
def main_page():
  if "code" in request.args:
    try:
      code = request.args["code"]

      data = exchange_code(code)

      access_token = data['access_token']


      

      data = getMe(access_token)

      print(data['avatar'])

      user = f"{data['username']}#{data['discriminator']}"
      
      data = [user, f"https://discord.com/widget?id=821872779523522580&theme=dark&username={user.split('#')[0].replace(' ', '%20')}",  f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"]

      return render_template("main.html", data=data)

    except:
      return render_template("main.html", data=None)
  else:
    return render_template("main.html", data=None)


  



@app.route('/<id>/<avatar>/')
def user(id, avatar):
  try:
    return render_template('users.html', data=[id,  f"https://cdn.discordapp.com/avatars/{id}/{avatar}.png", list(reading(id))])
  except:
    return render_template('404.html')



if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)

 #<div id="wrapper"><h1>Server Count: {{data}}</p></div>