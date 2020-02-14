import httpx, json, pymysql
from bs4 import BeautifulSoup

'''
hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

response = httpx.get(url="https://www.radarbox24.com/data/flights/BAW178", headers=hdr)

soup = BeautifulSoup(response)
s = soup.find_all('script')
init = str(s[8])
j = init[20:(len(init) - 10)]
d = json.loads(j)
print('flight json info: ', d['current'])


print('https://cdn.radarbox24.com/photo/''hello')
'''

connection = pymysql.connect(host='localhost',
                             user='flightcompanion',
                             password='fc1234',
                             db='flightcompanion',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        cursor.execute('select fn_id, ac_id, dep_id, arr_id from flights where fn_id = \'BAW178\'')
        fl = cursor.fetchall()
        try:
            flight = fl[0]
            print('flight: ', flight)
        except IndexError:
            pass

        cursor.execute('select * from aircraft where ac_id = %s', flight['ac_id'])
        ac = cursor.fetchall()
        try:
            aircraft = ac[0]
            print('aircraft: ', aircraft)
        except IndexError:
            pass

        cursor.execute('select * from flnum where fn_id = %s', flight['fn_id'])
        fn = cursor.fetchall()
        try:
            flight_num = fn[0]
            print('flight num: ', flight_num)
        except IndexError:
            pass

        print('arr id: ', flight['arr_id'])
        cursor.execute('select * from arr where arr_id = %s', flight['arr_id'])
        arr = cursor.fetchall()
        arrival = arr[0]

        cursor.execute('select * from dep where dep_id = %s', flight['dep_id'])
        dep = cursor.fetchall()
        departure = dep[0]
finally:
    None

flight_dict = {'flight': flight, 'aircraft': aircraft, 'flight_num': flight_num, 'arrival': arrival, 'departure': departure}
print(flight_dict)
link = (str(flight_dict['aircraft']['ac_photo']))
print(link)
if link[33: 37] == 'None':
    flight_dict['aircraft']['ac_photo'] = None

print('flight dict: ', flight_dict)


