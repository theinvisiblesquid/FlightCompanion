import json, pymysql, urllib.request, scraper
import logging

from bs4 import BeautifulSoup

from reader import Reader


class Populate():
    def checkifexists(self, json):
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        # ac are individual flight objects
        for ac in json['aircraft']:
            try:
                Populate.populatelog(None, ('Flight number from dump1090: ', ac['flight']))
                flight_number = ac['flight']
            except KeyError:
                flight_number = Populate.get_flight_number(None, ac['hex'])
                Populate.populatelog(None, ('Flight number was retrieved from ADSBX: ', flight_number))
            except Exception as e:
                Populate.populatelog(None, "Unhandled exception when getting flight number")


            # prints flight number from flight object
            # print('ac flight: ', ac['flight'])

            check = "select fn_id from flights where fn_id = %s"

            if not flight_number == '':
                if not flight_number is None:
                    with connection.cursor() as cursor:
                        cursor.execute(check, flight_number)

                        # if the flight doesn't exist, do something
                        if cursor.rowcount == 0:
                            Populate.populatelog(None, ('Flight ', flight_number, 'doesn\'t exist in the database'))
                            scraper.Scrape.scrape(None, flight_number, ac)
                        else:
                            Populate.populatelog(None, ('Flight', flight_number, 'is already in the database.'))
                else:
                    Populate.populatelog(None, 'A flight number couldn\'t be retrieved.')
                    break
            else:
                Populate.populatelog(None, 'A flight number couldn\'t be retrieved.')
                break
        connection.close()

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
            connection.close()

    def insert(self, curr, adsb, fn):
        print('scraped info to be inserted: ', curr)
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            flights = [fn, str(adsb['hex']), str(curr['aporgic']), str(curr['apdstic'])]

            flnum = [fn, str(curr['fnia']), str(curr['fnic']), str(curr['departure']),
                     str(curr['depdate']), str(curr['arrival']), str(curr['arrdate']), curr['distance']]

            aircraft = [str(adsb['hex']), str(curr['acr']), str(curr['acd']), str(curr['act']),
                        ('https://cdn.radarbox24.com/photo/' + str(curr['th1'])), str(curr['alna'])]

            arr = ['apdstic', 'apdstia', 'apdstna', 'apdsttzns']
            print('ARR INFORMATION FOR FLIGHT ', fn, ' GOING INTO ARR TABLE: ', tuple(curr.get(key) for key in arr))

            dep = ['aporgic', 'aporgia', 'aporgna', 'aporgtzns']

            Populate.populatelog(None, ('FLNUM DICT: ', flnum))

            ac = "INSERT INTO aircraft VALUES (%s, %s, %s, %s, %s, %s)"
            fn = "INSERT INTO flnum VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            ar = "INSERT INTO arr VALUES (%s, %s, %s, %s)"
            de = "INSERT INTO dep VALUES (%s, %s, %s, %s)"
            fl = "INSERT INTO flights (fn_id, ac_id, dep_id, arr_id) VALUES (%s, %s, %s, %s)"

            with connection.cursor() as cursor:
                try:
                    cursor.execute(ac, tuple(aircraft))
                    cursor.execute(fn, tuple(flnum))
                    cursor.execute(ar, tuple(curr.get(key) for key in arr))
                    cursor.execute(de, tuple(curr.get(key) for key in dep))
                    cursor.execute(fl, flights)
                    connection.commit()
                except pymysql.IntegrityError:
                    # Populate.populatelog(None, "SQl Integrity error: ", pymysql.IntegrityError.with_traceback())
                    print('integrity error')
                    pass
                except Exception as e:
                    Populate.populatelog(None, "Unhandled exception: ", e.with_traceback())
                    pass
        except KeyError:
            Populate.populatelog(None, ('***KEY ERROR IN SCRAPE***', KeyError.with_traceback()))
            print('***KEY ERROR IN SCRAPE***', KeyError.with_traceback())
        except Exception as e:
            Populate.populatelog(None, "Unhandled exception: ", e.with_traceback())
        finally:
            connection.close()

    def get_flight_number(self, icao):
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

   ,
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'api-auth': '9fffe36b-a50c-417a-894f-56260ca5a96d'}

        str(icao)
        url = ('https://adsbexchange.com/api/aircraft/icao/' + icao.upper() + '/')

        # print('***URL***', url)
        r = urllib.request.Request(url, headers=hdr)

        req = urllib.request.urlopen(r).read()
        string = str(req)
        json_untouched = string[2:-1]
        d = json.loads(json_untouched)

        # print('***DATA***', d)

        try:
            # print(d['ac'][0]['call'])
            return d['ac'][0]['call']
        except TypeError:
            Populate.populatelog(None, ("Type error when attempting to get flight number from adsbx for hex: ", icao))
            return None
        except Exception as e:
            Populate.populatelog(None, ("Unhandled exception when attempting to get flight number from adsbx for hex: ",
                                        icao))

    def populatelog(self, message):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='./populater.log',
                            filemode='a')

        logging.debug(message)
