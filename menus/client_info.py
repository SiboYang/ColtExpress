import json
import pickle
from _pickle import UnpicklingError
from threading import Thread, Condition, Lock, Event
import selectors
import socket
import pprint
import time
from assets.network_constants import *
from helpers.admin_login_helper import *

username = ""
password = ""
access_token = ""
refresh_token = ""
session = {}
server_ip = ""
server_port = ""
server_socket_connection = None
my_player_id = ""


class Client(Thread):
    __instance = None

    def __init__(self):
        Thread.__init__(self)
        self.username = ""
        self.password = ""
        self.access_token = ""
        self.refresh_token = ""
        self.session = {}
        self.connected = False
        self.game_manager_addr = ("", 0)
        self.socket = None
        self.selector = selectors.DefaultSelector()

        self.__condition = Condition(Lock())
        self.connect_event = Event()

        self.sync_buffer = None
        self.recv_buffer = None
        self.send_buffer = None

    @staticmethod
    def get_instance():
        if Client.__instance is None:
            Client.__instance = Client()
            Client.__instance.start()
        return Client.__instance

    def launch_session(self):
        response = requests.get(GAMEMANAGERURL + "/api/startgame/" + self.session)
        if response.status_code == 200:
            data = json.loads(response.json())
            self.game_manager_addr = (data['address'], int(data['port']))
            self.connect_event.set()

            return True
        else:
            print(response.text)
            return False

    def get_access_token(self):
        pass

    # MIGHT THROW KEY ERROR
    def login(self, username, password):
        if self.username != "" or self.password != "":
            return False, None
        res = get_user_access_token(username, password)
        if res.status_code == 200:
            self.username = username
            self.password = password
            self.access_token = res.json()['access_token']
            self.refresh_token = res.json()['refresh_token']

            return True, res
        else:
            return False, res

    # MIGHT THROW KEY ERROR
    def sign_up(self, username, password):
        res = signup_user(username, password)
        if res.status_code == 200:
            return True, res
        else:
            return False, res

    def connect_to_game(self):
        if self.game_manager_addr == ("", 0):
            print("Game manager address is not set !")
            return False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)
        print(self.game_manager_addr)
        try:
            self.socket.connect(self.game_manager_addr)
            print("Client connected.")
            self.connected = True
            return True
        except Exception as e:
            print("Something went wrong while connecting to the server.")
            print(e)
            self.socket.close()
            return False

    def receive_data(self):
        data = None
        while data is None:
            with self.__condition:
                data = self.sync_buffer
        return data

    def recv_data(self):
        try:
            # Should be ready to read
            payload_list = []
            buffer_size = 4096
            while True:
                pickled = self.socket.recv(buffer_size)
                payload_list.append(pickled)
                if len(pickled) < buffer_size:
                    break
            data = pickle.loads(b''.join(payload_list))
            pprint.pprint(data)
            return data
        except UnpicklingError:
            return self.recv_data()
        except EOFError:
            return self.recv_data()
        except BlockingIOError:
            pass
        '''else:
            if data:
                self.recv_buffer = data
                return data
            else:
                # TODO: time.sleep implementation dk what to do exactly
                time.sleep(1)
                # raise RuntimeError("Peer closed.")'''

    def send_data(self, data):
        if data is not None:
            try:
                # Should be ready to write
                self.socket.send(pickle.dumps(data))
            except BlockingIOError:
                pass

    def save(self):
        save_dict = {'type': 'save', 'data': ''}
        self.send_data(save_dict)

    def exit(self):
        exit_dict = {'type': 'exit', 'data': ''}
        self.send_data(exit_dict)

    def create_session(self, saveid=""):
        headers = {
            'Content-Type': 'application/json',
        }
        params = (
            ('access_token', self.access_token),
        )
        data = {"game": "ColtExpress", "creator": self.username, "savegame": saveid}
        response = requests.post(LOBBYURL + "/api/sessions", headers=headers, params=params,
                                 json=data)
        if response.status_code == 200:
            self.session = response.text
            print(self.session)
            return True, response
        else:
            print(response.text)
            return False, response

    def join_session(self, session):
        self.session = session["session"]
        url = LOBBYURL + "/api/sessions/" + str(self.session) + "/players/" + self.username
        params = (
            ('access_token', self.access_token),
        )
        return requests.put(url, params=params)

    def run(self):
        print("Client started.")
        connected = False
        while True:
            if not connected and self.connect_event.isSet():
                connected = self.connect_to_game()
            elif connected:
                self.recv_buffer = self.recv_data()
                with self.__condition:
                    self.sync_buffer = self.recv_buffer
            time.sleep(2)
