import http
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
import pymysql.cursors
import pymysql
import json
import socket
import base64
import pickle
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# Connect to the database
connection = pymysql.connect(host='den1.mysql6.gear.host',
                             user='flightcompanion',
                             password='Kw6t-PpS_47r',
                             db='flightcompanion',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
print("db connection", connection)

msg = s.recv(102400)
out = msg.decode('utf-8')
print('RECEIVED')
print(out)
n, d = out.split(',', 1)
print('name: ' + n)
print('data: ' + d)
#j = json.dumps(d, sort_keys=True)
#print('json: ' + d)
y = eval(d)
x = json.dumps(y)
print(y)
print('json: ' + x)
for k in x["aircraft"]:
    print(k["hex"])

# print('json?: ' + j['aircraft'])
# print('out: ', t)


# def insert_json():
#   with open('dump1090/aircraft.json') as json_file:
#      data = json.load(json_file)
#     for p in data['aircraft']:
#        print('Hex: ' + p['hex'])
#       print('Flight: ' + p['flight'])
##         with connection.cursor() as cursor:
#            sql = "INSERT INTO `aircraft` (`hex`, `flight`) VALUES (%s, %s)"
#           cursor.execute(sql, (p['hex'], p['flight']))
#          connection.commit()
##    print('entered')
