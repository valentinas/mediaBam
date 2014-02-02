import BaseHTTPServer, tpb, sys, ConfigParser, thread, json, codecs, torrent, pprint, urllib2
from urlparse import urlparse, parse_qs
from utorrent import Utorrent as ut

config = ConfigParser.ConfigParser()
config.read("server.config")
port = int(config.get("params","port"))

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.server.socket.getsockname()[0]
        parsedUrl = urlparse(self.path)
        parameters=parse_qs(parsedUrl.query)
        #if it's not a query string, then I'll just serve a file
        allowedPaths = ['/templates/js.js', '/templates/style.css']
        if(self.path.find('?') == -1 and self.path in allowedPaths):
           self.send_response(200, 'OK')
           self.send_header('Content-type', 'text/javascript')
           self.end_headers()
           self.wfile.write(open('.' + self.path).read())
           return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", 'http://localhost')
        self.end_headers()
        searchResultsHTML = u'' 
        if("search" in parameters):
            searchResultsTemplate = codecs.open('templates/searchResult.tpl', encoding='utf-8').read()
            results = tpb.search(parameters['search'][0])
            downloadApiUrl = u'http://%s:%s/?download={magnetLink}' % (ip, port)
            rowId = 0
            for res in results:
                rowId += 1
                searchResultsHTML += searchResultsTemplate.format(
                    title = res['title'],
                    details = res['details'],
                    seeders = res['seeders'],
                    leechers = res['leechers'],
                    downloadUrl = downloadApiUrl.format(magnetLink = urllib2.quote(res['downloadLink'])+'&rowId='+str(rowId)),
                    rowId = rowId) 
        if("download" in parameters):
            torrent.addMagnetLink(parameters['download'][0], parameters['path'][0])
            self.wfile.write('{"success": true, "rowId":"row%s"}'%parameters['rowId'][0])
            return
        mainTemplate = codecs.open('templates/main.tpl', encoding='utf-8').read()
        status = pprint.pformat(torrent.getStatus())
        self.wfile.write(mainTemplate.format(searchResultsHTML = searchResultsHTML, status = status).encode('utf-8'))

HandlerClass = RequestHandler 
HandlerClass.protocol_version = "HTTP/1.0" 

ServerClass  = BaseHTTPServer.HTTPServer

server_local_address = ('127.0.0.1', port)
httpd_local = ServerClass(server_local_address, HandlerClass)
local_socket = httpd_local.socket.getsockname()
thread.start_new_thread(httpd_local.serve_forever,())
print "Thread 1 is Serving HTTP on", local_socket[0], "port", local_socket[1], "..."

try:
    ip = config.get("params","ip")
    server_remote_address = (ip, port)
    httpd_remote = ServerClass(server_remote_address, HandlerClass)
    remote_socket = httpd_remote.socket.getsockname()
    thread.start_new_thread(httpd_remote.serve_forever, ())
    print "Thread 2 is Serving HTTP on", remote_socket[0], "port", remote_socket[1], "..."
except ConfigParser.NoOptionError:
    print "no ip was provided in server.config, so serving only on localhost"
while 1:
    pass
