import requests

from flask import Flask, json, Response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
BASE = "http://127.0.0.1:5000"
LOBBYBASE = "http://127.0.0.1:4242"
LOGINPARAMS = {"grant_type": "password", "username": "admin", "password": "admin"}
games = {}


class Game(Resource):
    def put(self, gameid):
        if self.request.headers["Content-Type"] == "application/json":
            game_put_parser = reqparse.RequestParser()
            game_put_parser.add_argument("creator", required=True, help="creator cannot be blank!", location=json)
            game_put_parser.add_argument("gameServer", required=True, help="gameServer cannot be blank!", location=json)
            game_put_parser.add_argument("players", type=list, required=True, help="Players cannot be blank!",
                                         location=json)
            game_put_parser.add_argument("savegame", location=json)
            args = game_put_parser.parse_args()
            args["GameState"] = {}
            games[gameid] = args
            return gameid, 200

    def delete(self, gameid):
        try:
            del games[gameid]
            return gameid, 200
        except KeyError:
            return "Game does not exist", 201


@api.resource('/api/status')
class Status(Resource):
    def get(self):
        return Response("Game Service alive and kicking", status=200, mimetype='text/plain')


api.add_resource(Game, "/api/games/<string:gameid>")


# api.add_resource(Status, "/api/status")

def lobbyonline():
    resp = requests.get(LOBBYBASE + "/api/online")
    if resp.status_code != 200:
        print("Api Offline")
        exit()
    else:
        print(resp.content)


def adminlogin():
    resp = requests.post(LOBBYBASE + "/oauth/token", auth=('bgp-client-name', 'bgp-client-pw'), params=LOGINPARAMS)
    authentication_data = resp.json()
    access_token = authentication_data["access_token"]
    refresh_token = authentication_data["refresh_token"]
    print("Authentication Status Code:", str(resp.status_code))
    return access_token, refresh_token


def registeratls(access_token):
    params = {"access_token": access_token}
    headers = {'Content-Type': 'application/json'}
    data = {"name": "ColtExpress", "location": BASE, "minSessionPlayers": "2", "maxSessionPlayers": "5",
            "webSupport": "true"}
    resp = requests.put(LOBBYBASE + "/api/gameservices/ColtExpress", headers=headers, params=params, json=data)
    print("Registration Status Code", str(resp.status_code))


lobbyonline()
access_token, refresh_token = adminlogin()

registeratls(access_token)

if __name__ == "__main__":
    app.run(debug=True)  # Remove debug flag for production
