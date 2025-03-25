# WSL - Windows Search Lol

A high-performance file system search and monitoring tool that provides instant file searching capabilities by maintaining a real-time cache of your file system.

## Features

- **Fast File Search**: Search through your entire file system in milliseconds
- **Real-time File System Monitoring**: Automatically updates the cache as files are created, modified, or deleted
- **Smart Search Results**: Results are categorized into:
  - Exact filename matches
  - Filename contains matches
  - Path contains matches
- **Cross-platform Support**: Works on both Windows and Unix-like systems
- **Efficient Caching**: Uses a memory-efficient approach to maintain the file system cache
- **Privilege Handling**: Automatically handles elevated privileges when needed

## Requirements

- Python 3.10 or higher
- Windows or Unix-like operating system
- Administrative privileges (for initial cache creation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wsl.git
cd wsl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Building Executables

### Windows
```bash
build.bat
```

### Unix/Linux
```bash
./build.sh
```

This will create two executables in the `dist` directory:
- `myWSL.exe` - The main search executable
- `WSL_init.exe` - The initialization executable

## Usage

### First-time Setup

1. Run the initialization executable to create the initial file system cache and start the file system monitoring:
```bash
# Windows
WSL_init.exe

# Unix/Linux
./WSL_init
```

2. The initialization process will scan your file system and create a cache. This may take some time depending on your system size.
3. **Important**: Keep the initialization process running in the background to maintain real-time file system monitoring. The process will automatically update the cache as files are created, modified, or deleted.

### Searching Files

1. With the initialization process running in the background, run the search executable in a separate terminal:
```bash
# Windows
myWSL.exe

# Unix/Linux
./myWSL
```

2. Enter your search term when prompted. The tool will search through the cached file system and display results in three categories:
   - Exact filename matches (green)
   - Filename contains matches (yellow)
   - Path contains matches (red)

## How It Works

1. The tool maintains a cache of your file system structure in `data/fileSystemCache.txt`
2. A file system watcher monitors for changes and updates the cache in real-time
3. When searching, the tool uses this cache instead of scanning the file system directly, providing near-instant results
4. The cache is automatically updated when files are created, modified, or deleted

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
