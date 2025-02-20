from listener import Watcher
from const import FILESYSTEM_CACHE_PATH

from cache import writeFileSystemCache

def main() -> None:
    print("We are creating the cache this might take a while.")
    writeFileSystemCache(FILESYSTEM_CACHE_PATH)
    print("Cache created.")

    w = Watcher()
    w.run()


if __name__ == '__main__':
    main()