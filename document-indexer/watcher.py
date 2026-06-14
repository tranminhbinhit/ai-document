from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from pathlib import Path

from processor import process_file


WATCH_FOLDER = os.getenv("WATCH_FOLDER", r"D:\DOC-MCP")


class DocumentHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        print(
            "New file:",
            event.src_path
        )

        process_file(
            event.src_path
        )


    def on_modified(self,event):

        if event.is_directory:
            return

        print(
            "Modified:",
            event.src_path
        )

        process_file(
            event.src_path
        )



observer = Observer()

observer.schedule(
    DocumentHandler(),
    WATCH_FOLDER,
    recursive=True
)

observer.start()


print(
    "Watching:",
    WATCH_FOLDER
)


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()


observer.join()