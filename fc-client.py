import os
import socket
import json
import pickle
from glob import glob
import pandas as pd
import base64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))
s.listen(5)


def run(str2):
    print(str2)
    while True:
        clientsocket, address = s.accept()
        print("Connection from", {address}, "has been established!")
        clientsocket.send(bytes(str2, 'utf-8'))
        print("sent", str2, "to server")


def get(str1='', str2=''):
    #for f_name in glob('./dump1090/*.json'):
    uid = 'hiddensquid'
    f_name = './dump1090/aircraft.json'
    with open(f_name) as json_data:
        data = json.load(json_data)
        e = str(data)
        print('DATA: ' + e)
        print(f_name, ' ', data['aircraft'])
        str1 += str(data)
        str2 += str(uid + ',' + str1)
    run(str2)


get()
