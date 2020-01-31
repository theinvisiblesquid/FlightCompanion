import time, json, populater, pymysql


class Reader():
    def read_log(self):
        while True:
            # open file with name
            f_name = './dump1090/aircraft.json'

            # open file, contents = json_data, give data var value of the contents turned into json
            with open(f_name) as json_data:
                adsb = json.load(json_data)

            # print information from file
            print('current: ', adsb)

            Reader.insertlive(None, adsb)

            populater.Populate.checkifexists(None, adsb)

            print('sleeping')
            time.sleep(1)

    def insertlive(self, adsb):
        print('adsb being inserted: ', adsb)

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

                    print(p['hex'], p['flight'])

                    sql = "INSERT INTO `adsb` (`hex`, `squawk`, `flight`, `lat`, `lon`, `nucp`, `seen_pos`, " \
                          "`altitude`, `vert_rate`, `track`, `speed`, `messages`, `seen`, `rssi`) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"

                    # print('tuple: ', tuple(p.get(key) for key in keys))
                    cursor.execute(sql, tuple(p.get(key) for key in keys))
                    print('EXECUTED')
            connection.commit()
        finally:
            print('LIVE FLIGHTS ENTERED')


if __name__ == '__main__':
    Reader.read_log(Reader)
