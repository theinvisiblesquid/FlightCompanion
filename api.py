import json, urllib, pymysql
from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Flights(Resource):
    def get(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json
                q = cursor.execute('select hex, flight, lat, lon from aircraft')
                result = cursor.fetchall()
                print('result: ', result)
                row_head = [x[0] for x in cursor.description]
                connection.close()
        finally:
            print('finally')

        print('row headers: ', row_head)
        json_data = []
        for r in result:
            json_data.append(dict(zip(row_head, r)))

        print('json data: ', json_data)
        print('dumped: ', json.dumps(json_data))

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
                    soup = BeautifulSoup(page, 'lxml')
                    s = soup.find_all('script')
                    init = str(s[8])
                    j = init[20:(len(init) - 10)]
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
        soup = BeautifulSoup(page, 'lxml')
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
