import time

from const import FILESYSTEM_CACHE_PATH

def findFilesFuzzy(searchTerm: str) -> list[str]:
    dirsFound: list[str] = []

    with open(FILESYSTEM_CACHE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if searchTerm.lower() in line.lower():
                dirsFound.append(line.strip())

    return dirsFound

def sortDirsByImportance(searchTerm: str, dirs: list[str]) -> tuple[list[str], list[str], list[str]]:
    dirFilenameMatches: list[str] = []
    dirFilenameContains: list[str] = []
    dirPathContains: list[str] = []

    for dir in dirs:
        filename = dir.split('\\')[-1].split('.')[0]
        
        if filename.lower() == searchTerm.lower():
            dirFilenameMatches.append(dir)
        
        elif searchTerm.lower() in filename.lower():
            dirFilenameContains.append(dir)
        
        elif searchTerm.lower() in dir.lower():
            dirPathContains.append(dir)

    return (dirFilenameMatches, dirFilenameContains, dirPathContains)

def main() -> None:
    searchTerm: str = input("Enter the search term (i.e. filename or folder name): ")
    dirsToPrint: list[str] = [] # This whole thing with the list looks dumb, but it's so that we can tell how long it takes to search all of the files, not how long it takes to print them.

    searchStartTime: float = time.time()
    dirsToPrint = findFilesFuzzy(searchTerm)
    filepathsFilenameMatches, filepathsFilenameContains, filepathsPathContains = sortDirsByImportance(searchTerm, dirsToPrint)
    searchEndTime: float = time.time()
    
    print("\nPath contains search term:")
    for dir in filepathsPathContains:
        print(dir)
    
    print("\nFilename contains search term:")
    for dir in filepathsFilenameContains:
        print(dir)
    
    print("\nExact filename matches:")
    for dir in filepathsFilenameMatches:
        print(dir)

    print(f'Your seach took {round(searchEndTime - searchStartTime, 2)} seconds.')

if __name__ == '__main__':
    main()