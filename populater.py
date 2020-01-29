import json, urllib3, pymysql
from bs4 import BeautifulSoup


class Populate():
    def checkIfExists(self, json):
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
                    Populate.insert(None, ac['flight'])

    def insert(self, fn):
        print(json, 'doesn\'t exist in the db')


    def scrape(self, fn):
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
        req = urllib3.request.Request(link, headers=hdr)
        try:
            page = urllib3.request.urlopen(req).read()
            # r = requests.get(link)
            # print(r)
            soup = BeautifulSoup(page, 'lxml')
            s = soup.find_all('script')
            init = str(s[8])
            j = init[20:(len(init) - 10)]
            d = json.loads(j)
            print('flight json info: ', d)
        finally:
            print('finished scraping')