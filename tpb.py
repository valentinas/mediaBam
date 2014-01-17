import urllib2, ConfigParser
from bs4 import BeautifulSoup as bs



config = ConfigParser.ConfigParser()
config.read("tpb.config")

def search(query):
    urlEncodedQuery = urllib2.quote(query.encode("utf8"))
    dom = bs(urllib2.urlopen(config.get('urls','search').format(urlEncodedQuery)))
    torrents = [];
    for torrent in dom.select('#searchResult > tr'):
        torrentDom = bs(str(torrent))
        downloadLink = torrentDom.select('td > a')[0]['href']
        title = torrentDom.select('.detLink')[0].get_text()
        seeders = torrentDom.select('td[align]')[0].get_text()
        leechers = torrentDom.select('td[align]')[1].get_text()
        details = torrentDom.select('.detDesc')[0].get_text()
        torrents.append({'downloadLink': downloadLink, 'title': title, 'seeders': seeders, 'leechers': leechers, 'details': details})
    return torrents
