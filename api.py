import json, urllib, pymysql
from bs4 import BeautifulSoup
# flask is similar to jsp's in java, it allows you to set up a URL's that when visited, run some python code and return a json object
from flask import Flask
from flask_restful import Resource, Api

# not sure what this is really, but it won't work without it. I think it's just setting up the app
app = Flask(__name__)
api = Api(app)


# defining a flights class to select data from my db
class Flights(Resource):
    #def is for creating methods (same as java), runs some code, returns a value
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

        '''
        print('row headers: ', row_head)

        # init json object that we will populate and return
        json_data = []

        # for each loop
        for r in result:
            # append the result onto the end of the json object
            # dict(zip(row_head, r)) haven't a notion what this does, but do it
            json_data.append(dict(zip(row_head, r)))

        print('json data: ', json_data)
        print('dumped: ', json.dumps(json_data))
        '''

        return result


class RBInfo(Resource):
    def get(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute("select flight from aircraft;")
            res = cursor.fetchall()
            # print(row['hex'])
            print(hex)
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                              'Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}

            for row in res:
                fl = row['flight']
                print(fl)
                link = ("https://www.radarbox24.com/data/flights/" + fl)
                print('Link: ', link)
                req = urllib.request.Request(link, headers=hdr)
                try:
                    page = urllib.request.urlopen(req).read()
                    # r = requests.get(link)
                    # print(r)
                    soup = BeautifulSoup(page)
                    s = soup.find_all('script')
                    init = str(s[8])
                    print('init: ', init)
                    j = init[20:(len(init) - 10)]
                    print('json: ', j)
                    d = json.loads(j)
                    print(d)
                except FileNotFoundError:
                    print()

            return d


@app.route('/flight/<flight>', methods=['GET'])
def flight(flight):
    print(flight)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    link = ("https://www.radarbox24.com/data/flights/" + flight)
    print('Link: ', link)
    req = urllib.request.Request(link, headers=hdr)
    try:
        page = urllib.request.urlopen(req).read()
        # r = requests.get(link)
        # print(r)
        soup = BeautifulSoup(page)
        s = soup.find_all('script')
        print('script = ', s)
        init = str(s[8])
        j = init[20:(len(init) - 10)]
        d = json.loads(j)
        curr = d['current']
        print('json from rb24: ', curr)
        #for p in d['current']:
            #print(p['acd'])

    except FileNotFoundError:
        print()

    return curr


api.add_resource(Flights, '/flights')
api.add_resource(RBInfo, '/info')
# api.add_resource(FlightInfo, '/flight/<flight>')

if __name__ == '__main__':
    app.run(port='5002')
