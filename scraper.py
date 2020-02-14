import urllib, json, logging, populater
from bs4 import BeautifulSoup


class Scrape():
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
            Scrape.scraperlog(None, ('Attempting to scrape RadarBox with URL: ', link))
            page = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')
            s = soup.find_all('script')
            # print('script tags: ', s)
            # print('8th tag: ', s[8])
            init = str(s[8])
            j = init[20:(len(init) - 10)]
            d = json.loads(j)
            # print('flight json info: ', d)
            curr = d['current']
            print('curr: ', curr)
            populater.Populate.insert(None, curr, adsb, fn)
        except IndexError:
            Scrape.scraperlog(None, ('There was an index error while reading RadarBox\'s JSON', IndexError.with_traceback(None, None)))
        except TimeoutError:
            Scrape.scraperlog(None,
                              (('There was a timeout error for URL: ', link), TimeoutError.with_traceback(None, None)))
        except Exception as e:
            Scrape.scraperlog(None, (
            ('There was an unhandled exception when scraping URL: ', link), e.with_traceback(None, None)))
        finally:
            Scrape.scraperlog(None, ('Finished scraping info for flight ', fn))

    def scraperlog(self, message):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='./scraper.log',
                            filemode='a')

        logging.debug(message)
