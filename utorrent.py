import time, urllib2, base64
from bs4 import BeautifulSoup as bs

config = ConfigParser.ConfigParser()
config.read("utorrent.config")
url = config.get("webui","url") + '/gui/' 
authString = base64.b64encode(config.get("webui","username") + ':' + config.get("webui","password"))

class Utorrent:
    def __init__(self):
       self.authRequest = Utorrent.doAuthRequest()
       self.token = self.getToken()
       self.cookie = self.getCookie()
   
    @staticmethod
    def doAuthRequest():
        url = webUiUrl + 'token.html?t=' + str(int(time.time()))
        request = urllib2.Request(url)
        request.add_header('Authorization', 'Basic ' + authString)
        return urllib2.urlopen(request)

    def getToken(self):
        parsedAuthRequest = bs(self.authRequest)
        return parsedAuthRequest.div.get_text()

    def getCookie(self):
        return self.authRequest.info()['Set-Cookie']
    
    def download(self, url):
        downloadUrl = webUiUrl + '?token='+ self.token + '&action=add-url&s=' + url
        print downloadUrl
        addTorrentRequest = urllib2.Request(downloadUrl)
        
        addTorrentRequest.add_header('Cookie', self.cookie)
        addTorrentRequest.add_header('Authorization', 'Basic ' + authString)
        result = ""
        try:
            result = urllib2.urlopen(addTorrentRequest).read()
        except urllib2.HTTPError, err:
            result = err
        return result
