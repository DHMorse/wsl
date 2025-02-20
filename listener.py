import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from const import FILESYSTEM_CACHE_PATH as fileSystemCacheFile

def remove_line(filename: str, deletedFilePath: str) -> None:
    """Remove a specific line from a binary file."""
    # Convert to bytes if working with binary files
    deleted_path_bytes = deletedFilePath.encode('utf-8') + b'\n'
    
    # Read all lines
    with open(filename, 'rb') as file:
        lines = file.readlines()
    
    # Look for the line to remove
    for index, line in enumerate(lines):
        if line == deleted_path_bytes:
            # Remove the specified line
            lines.pop(index)
            print(f"Line '{deletedFilePath}' removed from '{filename}' successfully.")
            break
    
    # Write the modified content back to the file
    with open(filename, 'wb') as file:
        file.writelines(lines)

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\" if os.name == "nt" else "/"  # Adjust for Windows or Unix-based systems

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

        # Remove the deleted file from the cache
        remove_line(fileSystemCacheFile, event.src_path)

    @staticmethod
    def on_moved(event):
        global fileSystemCacheFile
        print(f"File moved from {event.src_path} to {event.dest_path}")

        # Remove the old file path from the cache
        remove_line(fileSystemCacheFile, event.src_path)

        # Add the new file path to the cache
        with open(fileSystemCacheFile, "a", encoding="utf-8") as file:
            file.write(event.dest_path + "\n")

if __name__ == '__main__':
    w = Watcher()
    w.run()