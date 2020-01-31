import json, pymysql, urllib
from bs4 import BeautifulSoup


class Populate():
    def checkifexists(self, json):
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        print('check: ', json['aircraft'])

        # ac are individual flight objects
        for ac in json['aircraft']:

            print('ac: ', ac)

            # prints flight number from flight object
            print('ac flight: ', ac['flight'])

            check = "select fn_id from flights where fn_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(check, ac['flight'])

                # if the flight doesn't exist, do something
                if cursor.rowcount == 0:
                    print('result is null')
                    Populate.scrape(None, ac['flight'], ac)
                else:
                    print('FLIGHT ALREADY IN DB')

    def scrape(self, fn, adsb):
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        link = ("https://www.radarbox24.com/data/flights/" + fn)
        print('Link: ', link)
        req = urllib.request.Request(link, headers=hdr)
        try:
            page = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')
            s = soup.find_all('script')
            # print('script tags: ', s)
            print('8th tag: ', s[8])
            init = str(s[8])
            j = init[20:(len(init) - 10)]
            d = json.loads(j)
            # print('flight json info: ', d)
            curr = d['current']
            print('curr: ', curr)
        finally:
            print('finished scraping')

        Populate.insert(None, curr, adsb)

    def insert(self, curr, adsb):
        print('scraped info to be inserted: ', curr)

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='flightcompanion',
                                     password='fc1234',
                                     db='flightcompanion',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        flights = [str(adsb['flight']), str(adsb['hex']), str(curr['apdstic']), str(curr['aporgic'])]

        flnum = [str(adsb['flight']), str(curr['fnia']), str(curr['fnic']), str(curr['departure']),
                 str(curr['depdate']), str(curr['arrival']), str(curr['arrdate']), curr['distance']]

        aircraft = [str(adsb['hex']), str(curr['acr']), str(curr['acd']), str(curr['act']),
                    ('https://cdn.radarbox24.com/photo/' + str(curr['th1'])), str(curr['alna'])]

        arr = ['apdstic', 'apdstia', 'apdstna', 'apdsttzns']

        dep = ['aporgic', 'aporgia', 'aporgna', 'aporgtzns']

        print('FLNUM DICT: ', flnum)

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
                pass
