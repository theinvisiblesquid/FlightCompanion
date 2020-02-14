import urllib.request, json

'''
ADSBx REST API request format

All Aircraft
https://adsbexchange.com/api/aircraft/json/

All Aircraft within x NM of point located at latitude, longitude ( 37.1661, -119.44944 )
https://adsbexchange.com/api/aircraft/json/lat/37.16611/lon/-119.44944/dist/10/

Aircraft with ICAO hex code
https://adsbexchange.com/api/aircraft/icao/A686AD/

Aircraft(s) broadcasting a squawk code
https://adsbexchange.com/api/aircraft/sqk/3522/

Aircraft(s) with ADSBx community registration information
https://adsbexchange.com/api/aircraft/registration/57-1469/

Aircraft tagged by ADSBx community as Military
https://adsbexchange.com/api/aircraft/mil/


***MUST BE UPPERCASE***
'''

hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'api-auth': '9fffe36b-a50c-417a-894f-56260ca5a96d'}

r = urllib.request.Request('https://adsbexchange.com/api/aircraft/icao/406B1F/', headers=hdr)

req = urllib.request.urlopen(r).read()

string = str(req)
json_untouched = string[2:-1]
d = json.loads(json_untouched)

print(d)

