from listener import main as listener
from const import FILESYSTEM_CACHE_PATH

from cache import writeFileSystemCache

def main() -> None:
    writeFileSystemCache(FILESYSTEM_CACHE_PATH)
    print("Cache created.")

    listener()

if __name__ == '__main__':
    main()