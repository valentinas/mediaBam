import BaseHTTPServer, tpb, sys, ConfigParser, thread
from urlparse import urlparse, parse_qs
from utorrent import Utorrent as ut

config = ConfigParser.ConfigParser()
config.read("server.config")
port = int(config.get("params","port"))

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.server.socket.getsockname()[0]
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        parameters=parse_qs(urlparse(self.path).query)
        result = '<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>\
                  <script type="text/javascript">\
                      jQuery(function(){jQuery("select.download").change(function(){jQuery.ajax({url:jQuery(this).val()})})})</script>\
                  <form action="/" method="get">\
                  search: <input type="text" name="search"><br>\
                  <input type="submit" value="Submit">\
                  </form>'
        if("search" in parameters):
            result += '<table><thead><tr><td>Title</td><td>Details</td><td>Seeders</td><td>Leechers</td><td>Download to</td></tr></thead>'
            results = tpb.search(parameters['search'][0])
            for res in results:
                result += u'<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td><select class="download"><option>===select===</option>><option value="{5}{4}&path=%2Fvideo%2Fmovies">movies</option><option value="{5}{4}&path=%2Fvideo%2Ftv">tv</option><option value="{5}{4}&path=%2Fmusic">music</option></select></td></tr>'.format( res['title'],  res['details'], res['seeders'], res['leechers'], res['downloadLink'], 'http://%s:%s/?download=' % (ip, port)) 
            result += '</tbody></table>'
        if("download" in parameters):
            client = ut()
            result = client.download(parameters['download'][0] + '&path=' +  parameters['path'][0])
        self.wfile.write(result.encode('UTF-8'))

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
