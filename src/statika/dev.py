from logging import getLogger
from os import path, getcwd, fork
from sys import argv, exit
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from statika import build


def start_watcher(watched_dir, bundles, build_func=None, logger=None,
                  file_patterns=['*.css', '*.js', '*.html']):
    if build_func is None:
        build_func = build
    if logger is None:
        logger = getLogger(__name__)

    def _build(event):
        filename = path.split(event.src_path)[1]
        if not event.src_path or filename[0] in ('.', '_'):
            return
        ext = path.splitext(filename)[1]
        logger.debug(' - %s is modified, rebuild static', event.src_path)
        build_func(bundles)

    def builder_process():
        build_func(bundles)
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

    if fork() == 0:
        builder_process()
        exit()


if __name__ == '__main__':
    if len(argv) > 1 and path.isdir(argv[1]):
        watched_dir = argv[1]
    else:
        watched_dir = getcwd()
    start_watcher(watched_dir, argv[2:])
