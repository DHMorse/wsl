from listener import Watcher

from cache import writeFileSystemCache

def main() -> None:
    print("We are creating the cache this might take a while.")
    writeFileSystemCache("fileSystemCache.txt")
    print("Cache created.")

    w = Watcher()
    w.run()


if __name__ == '__main__':
    main()