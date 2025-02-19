import os

def writeFileSystemCache(outputFile) -> None:
    rootDir = "C:\\" if os.name == "nt" else "/"  # Adjust for Windows or Unix-based systems
    
    with open(outputFile, "w", encoding="utf-8") as file:
        for dirpath, dirnames, filenames in os.walk(rootDir):
            file.write(f"{dirpath}\n")  # Write directory path
            for filename in filenames:
                file.write(f"{os.path.join(dirpath, filename)}\n")  # Write file path

if __name__ == "__main__":
    output_file = 'C:\\Users\\daniel\\scripts\\WSL\\fileSystemCache.txt'
    writeFileSystemCache(output_file)
    print(f"All file paths saved to {output_file}")
