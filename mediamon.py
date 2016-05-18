# /usr/local/mediamon.py
# Location /usr/local/mediamon/mediamon.py

from datetime import datetime
import os.path
import sys
from subprocess import call
import signal
import configparser
import pyinotify


log_file = open("/var/log/mediamon.log", "a")

def log(text):
    dt = datetime.utcnow().isoformat()
    log_file.write(dt + ' - ' + text + "\n")
    log_file.flush()

def signal_handler(signal, frame):
    log("Exiting")
    sys.exit(0)

log("Starting")

signal.signal(signal.SIGTERM, signal_handler)

Config = configparser.ConfigParser()
Config.readfp(open('/usr/local/mediamon.cfg', 'r'))

watched_paths = [path for key, path in Config.items('watchfolders')]
allowed_exts = list(filter(None, (x.strip() for x in Config.get('allowedextensions','exts').splitlines())))
excl_lst = [regexp for key, regexp in Config.items('exclude')]

wm = pyinotify.WatchManager()
mask = (
    pyinotify.IN_MODIFY |
    pyinotify.IN_CLOSE_WRITE |
    pyinotify.IN_DELETE |
    pyinotify.IN_CREATE |
    pyinotify.IN_MOVED_TO |
    pyinotify.IN_MOVED_FROM
)


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        self.modified_files = set()

    def process_IN_CREATE(self, event):
        self.process_create(event)

    def process_IN_MOVED_TO(self, event):
        self.process_create(event)

    def process_IN_MOVED_FROM(self, event):
        self.process_delete(event)

    def process_IN_DELETE(self, event):
        self.process_delete(event)

    def process_create(self, event):
        arg = ''
        if event.dir:
            arg = "-A"
        else:
            arg = "-a"
        self.do_index_command(event, arg)

    def process_delete(self, event):
        arg = ''
        if event.dir:
            arg = "-D"
        else:
            arg = "-d"
        self.do_index_command(event, arg)

    def process_IN_MODIFY(self, event):
        if self.is_allowed_path(event.pathname, event.dir):
            self.modified_files.add(event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        # ignore close_write unless the file has previously been modified.
        if (event.pathname in self.modified_files):
            self.do_index_command(event, "-a")

    def do_index_command(self, event, index_argument):
        if self.is_allowed_path(event.pathname, event.dir):
            log("synoindex %s %s" % (index_argument, event.pathname))
            call(["synoindex", index_argument, event.pathname])

            if index_argument == "-A":
                call(["php", "/volume1/web/TweetAlbum/tweetnewalbum.php", "%s (%s)" % (event.name, event.pathname)])
                log("Tweet %s %s" % (event.name, event.pathname))

            self.modified_files.discard(event.pathname)
        else:
            log("%s is not an allowed path" % event.pathname)

    def is_allowed_path(self, filename, is_dir):
        # Don't check the extension for directories
        if not is_dir:
            ext = os.path.splitext(filename)[1][1:].lower()
            if ext not in allowed_exts:
                return False
        return True

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(
    watched_paths,
    mask,
    rec=True,
    auto_add=True,
    exclude_filter=pyinotify.ExcludeFilter(excl_lst)
)

try:
    notifier.loop(daemonize=True, pid_file='/var/run/mediamon.pid')
except pyinotify.NotifierError as err:
    print >> sys.stderr, err
