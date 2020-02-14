import logging
import time, json, populater, pymysql

import requests


class Reader():
    def read_log(self):
        while True:
            # open file with name
            f_name = './dump1090/aircraft.json'

            # open file, contents = json_data, give data var value of the contents turned into json
            with open(f_name) as json_data:
                adsb = json.load(json_data)

            print(adsb)
            # print information from file
            # Reader.readerlog(None, ('Current information of incoming ADS-B data: ', adsb))
            # Reader.insertlive(None, adsb)
            # populater.Populate.checkifexists(None, adsb)

            res = requests.post('http://localhost:5002/ep', json=adsb)
            print('response from server:', res.text)

            time.sleep(1)


    def insertlive(self, adsb):
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE adsb;")
                print('TRUNCATED')

                for p in adsb['aircraft']:
                    print('p: ', p)
                    keys = ['hex', 'squawk', 'flight', 'lat', 'lon', 'nucp', 'seen_pos',
                            'altitude', 'vert_rate', 'track', 'speed', 'messages', 'seen',
                            'rssi']

                    # print(p['hex'], p['flight'])

                    sql = "INSERT INTO `adsb` (`hex`, `squawk`, `flight`, `lat`, `lon`, `nucp`, `seen_pos`, " \
                          "`altitude`, `vert_rate`, `track`, `speed`, `messages`, `seen`, `rssi`) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"

                    # print('tuple: ', tuple(p.get(key) for key in keys))
                    cursor.execute(sql, tuple(p.get(key) for key in keys))
            connection.commit()
        finally:
            Reader.readerlog(None, 'Live flights entered into adsb table')

    def readerlog(self, message):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='./reader.log',
                            filemode='a')

        logging.debug(message)

if __name__ == '__main__':
    Reader.read_log(Reader)
