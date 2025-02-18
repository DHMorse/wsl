import time

def findFilesFuzzy(searchTerm: str) -> list[str]:
    dirsFound: list[str] = []

    with open("fileSystemCache.txt", "r", encoding="utf-8") as file:
        for line in file:
            if searchTerm in line:
                dirsFound.append(line.strip())

    return dirsFound

def main() -> None:
    searchTerm: str = input("Enter the search term (i.e. filename or folder name): ")
    dirsToPrint: list[str] = [] # This whole thing with the list looks dumb, but it's so that we can tell how long it takes to search all of the files, not how long it takes to print them.

    searchStartTime: float = time.time()
    dirsToPrint = findFilesFuzzy(searchTerm)
    searchEndTime: float = time.time()
    
    for dir in dirsToPrint:
        print(dir)

    print(f'Your seach took {round(searchEndTime - searchStartTime, 2)} seconds.')

if __name__ == '__main__':
    main()