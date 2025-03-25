"""
File system watcher module that monitors file system events and maintains a cache of file paths.
This module is designed to work cross-platform using the watchdog library to monitor
file system events in real-time.
"""

import time
import os
import sys
import logging
import argparse
from pathlib import Path
from typing import NoReturn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from const import FILESYSTEM_CACHE_PATH as fileSystemCacheFile

# convert fileSystemCacheFile to a Path object
fileSystemCacheFile = Path(fileSystemCacheFile)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def removeLineFromCache(cachePath: Path, targetPath: str) -> None:
    """
    Remove a specific line from the cache file.
    
    Args:
        cachePath: Path to the cache file
        targetPath: The file path to remove from the cache
    """
    try:
        if not cachePath.exists():
            return
            
        with open(cachePath, 'r', encoding='utf-8', newline='') as file:
            lines = file.readlines()
        
        # Filter out the target line, normalizing line endings
        targetPath = str(Path(targetPath))  # Normalize path separators
        updatedLines = [line.rstrip('\r\n') for line in lines if line.rstrip('\r\n') != targetPath]
        
        with open(cachePath, 'w', encoding='utf-8', newline='') as file:
            file.write('\n'.join(updatedLines) + '\n')
    except IOError as error:
        logger.error(f"Error updating cache file: {error}")

def appendToCache(cachePath: Path, filePath: str) -> None:
    """
    Append a file path to the cache file.
    
    Args:
        cachePath: Path to the cache file
        filePath: The file path to append to the cache
    """
    try:
        # Normalize path separators
        filePath = str(Path(filePath))
        with open(cachePath, "a", encoding="utf-8", newline='') as file:
            file.write(f"{filePath}\n")
    except IOError as error:
        logger.error(f"Error writing to cache file: {error}")

class FileSystemWatcher:
    """
    A class that monitors file system events using the watchdog library.
    Maintains a cache of file paths in a specified file.
    """
    
    def __init__(self, rootPath: str = os.path.expanduser("~")):
        """
        Initialize the file system watcher.
        
        Args:
            rootPath: The root directory to watch (defaults to user's home directory)
        """
        self.rootPath = Path(rootPath)
        if not self.rootPath.exists():
            raise FileNotFoundError(f"Directory does not exist: {self.rootPath}")
        if not self.rootPath.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.rootPath}")
        if not os.access(self.rootPath, os.R_OK):
            raise PermissionError(f"No read access to directory: {self.rootPath}")
            
        self.observer = Observer()
        self.eventHandler = FileSystemEventHandler()
        self._setupEventHandlers()
        logger.info(f"Initialized watcher for directory: {self.rootPath}")

    def _setupEventHandlers(self) -> None:
        """Set up the event handlers for file system events."""
        self.eventHandler.on_created = self._handleCreated
        self.eventHandler.on_deleted = self._handleDeleted
        self.eventHandler.on_moved = self._handleMoved

    def _handleCreated(self, event) -> None:
        """Handle file creation events."""
        logger.info(f"File created: {event.src_path}")
        appendToCache(fileSystemCacheFile, event.src_path)

    def _handleDeleted(self, event) -> None:
        """Handle file deletion events."""
        logger.info(f"File deleted: {event.src_path}")
        removeLineFromCache(fileSystemCacheFile, event.src_path)

    def _handleMoved(self, event) -> None:
        """Handle file move/rename events."""
        logger.info(f"File moved from {event.src_path} to {event.dest_path}")
        removeLineFromCache(fileSystemCacheFile, event.src_path)
        appendToCache(fileSystemCacheFile, event.dest_path)

    def start(self) -> NoReturn:
        """
        Start the file system watcher.
        This method runs indefinitely until interrupted.
        """
        try:
            self.observer.schedule(self.eventHandler, str(self.rootPath), recursive=True)
            self.observer.start()
            logger.info("Started watching for file system events")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping file system watcher...")
            self.observer.stop()
        except Exception as error:
            logger.error(f"Error in file system watcher: {error}")
            self.observer.stop()
        finally:
            self.observer.join()

def parseArguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Monitor file system events')
    parser.add_argument(
        '--directory',
        '-d',
        default=os.path.expanduser("~"),
        help='Directory to watch (default: user home directory)'
    )
    return parser.parse_args()

def main() -> None:
    """Main entry point for the file system watcher."""
    try:
        args = parseArguments()
        watcher = FileSystemWatcher(args.directory)
        watcher.start()
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        logger.error(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()