from logging import getLogger
from multiprocessing import Process
from os import path, getcwd
from sys import argv
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from statika import build

def start_watcher(watched_dir, bundles, build_func=None, logger=None,
                  file_patterns=['*.js', '*.css']):
    if build_func is None:
        build_func = build
    if logger is None:
        logger = getLogger(__name__)

    def _build(event):
        filename = path.split(event.src_path)[1]
        if not event.src_path or filename[0] in ('.', '_'):
            return
        ext = path.splitext(filename)[1]
        logger.debug(' - %s is modified, rebuild static' % event.src_path)
        build_func(bundles)

    def builder_process():
        logger.debug(' - Watched static files for changes to rebuild')
        event_handler = PatternMatchingEventHandler(
            patterns=file_patterns,
            ignore_directories=True
        )
        event_handler.on_modified = _build
        observer = Observer()
        observer.schedule(event_handler, path=watched_dir, recursive=True)
        observer.start()    
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

    build_func(bundles)
    _watcher = Process(target=builder_process, name='killa')
    _watcher.start()


if __name__ == '__main__':
    if len(argv) > 1 and path.isdir(argv[1]):
        watched_dir = argv[1]
    else:
        watched_dir = getcwd()
    start_watcher(watched_dir, argv[2:])
from logging import getLogger
from multiprocessing import Process
from os import path, getcwd
from sys import argv

from pyinotify import WatchManager, Notifier, IN_MODIFY, IN_CREATE, IN_DELETE

from statika import build


def start_watcher(watched_dir, bundles, build_func=None, logger=None,
                  file_types=('js', 'css', 'html')):
    if build_func is None:
        build_func = build
    if logger is None:
        logger = getLogger(__name__)

    def _build(event):
        if not event.name or event.name[0] in ('.', '_'):
            return
        ext = path.splitext(event.name)[1]
        if ext not in file_types:
            return
        logger.debug(' - %s is modified, rebuild static' % event.pathname)
        build_func(bundles)

    def builder_process():
        logger.debug(' - Watched static files for changes to rebuild')
        wm = WatchManager()
        notifier = Notifier(wm, default_proc_fun=_build)
        wm.add_watch(
            watched_dir,
            IN_MODIFY, # | IN_CREATE | IN_DELETE,
            rec=True, auto_add=True
        )
        notifier.loop()

    build_func(bundles)
    _watcher = Process(target=builder_process, name='killa')
    _watcher.start()


if __name__ == '__main__':
    if len(argv) > 1 and path.isdir(argv[1]):
        watched_dir = argv[1]
    else:
        watched_dir = getcwd()
    start_watcher(watched_dir, argv[2:])
