import libtorrent as lt
import time, pprint, thread, ConfigParser

config = ConfigParser.ConfigParser()
config.read("torrent.config")
downloadsFolderPath = config.get("settings","downloadsFolderPath")

def addMagnetLink(link, path):
    thread.start_new_thread(magnetWorker, (link, downloadsFolderPath + path,))

def getStatus():
    stateString = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']
    result = [{\
                'is_DHT_running': str(session.is_dht_running()),\
                'number_of_dht_nodes': str(session.status().dht_nodes),\
                'error': i.status().error,\
                'paused': str(i.status().paused),\
                'number_of_trackers': str(len(i.trackers())),\
                'name': i.name(),\
                'hash': i.info_hash(),\
                'progress': '%.2f%%' % (i.status().progress * 100), \
                'downloadRate': '%.1f kb/s' % (i.status().download_rate / 1000), \
                'uploadRate': '%.1f kb/s' % (i.status().upload_rate / 1000),\
                'numberOfPeers': i.status().num_peers,\
                'state': stateString[i.status().state]\
                }  for i in  session.get_torrents()]
    return(result)

def magnetWorker(link, path):
    params = {
        'save_path': path,
        'paused': False,
        'auto_managed': False,
    }
    handle = lt.add_magnet_uri(session, link, params)

def cleaningWorker():
    while 1:
        for t in  session.get_torrents():
            if(t.status().state == 5):
                session.remove_torrent(t)
        time.sleep(10)

session = lt.session()
session.listen_on(6881, 6891)
thread.start_new_thread(cleaningWorker, ())
