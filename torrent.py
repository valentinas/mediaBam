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
    print(path)
    params = {
        'save_path': path,
    }
    handle = lt.add_magnet_uri(session, link, params)
    while (not handle.has_metadata()):
        time.sleep(1)
    info = handle.get_torrent_info()
    handle = session.add_torrent({'ti': info, 'save_path': path})


session = lt.session()
session.listen_on(6881, 6891)
