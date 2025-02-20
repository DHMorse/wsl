import time

from const import FILESYSTEM_CACHE_PATH, COLORS

def fuzzySearchAndCategorizeResults(searchTerm: str) -> tuple[list[str], list[str], list[str]]:
    dirFilenameMatches: list[str] = []
    dirFilenameContains: list[str] = []
    dirPathContains: list[str] = []

    searchTerm = searchTerm.lower()

    with open(FILESYSTEM_CACHE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            lineLower = line.lower()
            if searchTerm in lineLower:
                line = line.strip()
                filename = lineLower.split('\\')[-1].split('.')[0]
                
                if filename == searchTerm:
                    dirFilenameMatches.append(line)
                
                elif searchTerm in filename:
                    dirFilenameContains.append(line)
                
                else:
                    dirPathContains.append(line)

    return (dirFilenameMatches, dirFilenameContains, dirPathContains)


def main() -> None:
    searchTerm: str = input("Enter the search term (i.e. filename or folder name): ")

    searchStartTime: float = time.time()
    filepathsFilenameMatches, filepathsFilenameContains, filepathsPathContains = fuzzySearchAndCategorizeResults(searchTerm)
    searchEndTime: float = time.time()
    
    print(f"\n{COLORS['red']}Path contains search term:{COLORS['reset']}")
    for dir in filepathsPathContains:
        print(dir)
    
    print(f"\n{COLORS['yellow']}Filename contains search term:{COLORS['reset']}")
    for dir in filepathsFilenameContains:
        print(dir)
    
    print(f"\n{COLORS['green']}Exact filename matches:{COLORS['reset']}")
    for dir in filepathsFilenameMatches:
        print(dir)

    print(f'Your seach took {round(searchEndTime - searchStartTime, 2)} seconds.')

if __name__ == '__main__':
    main()