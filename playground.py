import httpx, json
from bs4 import BeautifulSoup

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
