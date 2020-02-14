import json, urllib, pymysql, logging
from urllib import request
from bs4 import BeautifulSoup
# flask is similar to jsp's in java, it allows you to set up a URL's that when visited, run some python code and return a json object
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# not sure what this is really, but it won't work without it. I think it's just setting up the app
import populater

app = Flask(__name__)
api = Api(app)


# defining a flights class to select data from my db
class Flights(Resource):
    # def is for creating methods (same as java), runs some code, returns a value
    def get(self):
        # setting up the connection to the database
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        # put inside try catch in case of errors
        try:
            # connection and any subsequent SQL will run inside this with statement
            # cursor is essentially the variable storing our connection object, and we can do sql stuff with the cursor object
            with connection.cursor() as cursor:
                # https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json

                # execute the following SQL statement
                cursor.execute('select hex, flight, lat, lon from adsb')

                # fetch all the returned values and put them in the result variable
                result = cursor.fetchall()

                print('result: ', result)
                '''
                # get the row headers, these are the column names
                row_head = [x[0] for x in cursor.description]
                connection.close()
                '''
        finally:
            print('finally')

        connection.close()
        return result


@app.route('/flight/<flight>', methods=['GET'])
def flight(flight):
    print(flight)

    connection = pymysql.connect(host='localhost',
                                 user='flightcompanion',
                                 password='fc1234',
                                 db='flightcompanion',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute('select fn_id, ac_id, dep_id, arr_id from flights where fn_id = %s', flight)
            fl = cursor.fetchall()
            try:
                flight_record = fl[0]
                print('flight: ', flight)
            except IndexError:
                pass
            cursor.execute('select * from aircraft where ac_id = %s', flight_record['ac_id'])
            ac = cursor.fetchall()
            try:
                aircraft = ac[0]
                print('aircraft: ', aircraft)
            except IndexError:
                pass
            cursor.execute('select * from flnum where fn_id = %s', flight_record['fn_id'])
            fn = cursor.fetchall()
            try:
                flight_num = fn[0]
                print('flight num: ', flight_num)
            except IndexError:
                pass
            print('arr id: ', flight_record['arr_id'])
            cursor.execute('select * from arr where arr_id = %s', flight_record['arr_id'])
            arr = cursor.fetchall()
            arrival = arr[0]
            cursor.execute('select * from dep where dep_id = %s', flight_record['dep_id'])
            dep = cursor.fetchall()
            departure = dep[0]
    finally:
        connection.close()

    flight_dict = {'flight': flight_record, 'aircraft': aircraft, 'flight_num': flight_num, 'arrival': arrival,
                   'departure': departure}
    print(flight_dict)
    link = (str(flight_dict['aircraft']['ac_photo']))
    print(link)
    if link[33: 37] == 'None':
        flight_dict['aircraft']['ac_photo'] = None

    print('flight dict: ', flight_dict)
    return flight_dict


class RecordedFlights(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        get = 'select fn_id, ac_id, dep_id, arr_id from flights;'
        with connection.cursor() as cursor:
            cursor.execute(get)
            result = cursor.fetchall()

        return result

class Endpoint(Resource):
    def post(self):
        # get json data
        posted = request.get_json()
        print('JSON incoming via POST:', posted)
        # return {'message': 'POST data received', 'json': posted}

        populater.Populate.insertlive(None, posted)
        populater.Populate.checkifexists(None, posted)
        return {'message': 'POST received', 'data': posted}


api.add_resource(Flights, '/live')
api.add_resource(Endpoint, '/ep')
api.add_resource(RecordedFlights, '/flights')
# api.add_resource(FlightInfo, '/flight/<flight>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5002')
