import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

fileSystemCacheFile = "fileSystemCache.txt"

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\" if os.name == "nt" else "/"  # Adjust for Windows or Unix-based systems

    #DIRECTORY_TO_WATCH = "C:\\Users\\daniel\\Documents\\code\\wsl"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    
    @staticmethod
    def on_created(event):
        global fileSystemCacheFile
        print(f"File created: {event.src_path}")
        with open(fileSystemCacheFile, "a", encoding="utf-8") as file:
            file.write(event.src_path + "\n")

    @staticmethod
    def on_deleted(event):
        global fileSystemCacheFile
        print(f"File deleted: {event.src_path}")

        with open(fileSystemCacheFile, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        with open(fileSystemCacheFile, "w", encoding="utf-8") as file:
            for line in lines:
                if event.src_path.strip() != line.strip():
                    file.write(line)

if __name__ == '__main__':
    w = Watcher()
    w.run()