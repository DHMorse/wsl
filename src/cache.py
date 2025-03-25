import os
import subprocess
import platform
import concurrent.futures
import tempfile

def writeFileSystemCache(outputFile, max_workers=8) -> None:
    if not os.path.exists(outputFile):
        print(f"Creating directory: {os.path.dirname(outputFile)}")
        os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    
    print("We are creating the cache this might take a while.")

    # Check if script is already running with elevated privileges
    is_admin = False
    
    if platform.system() == "Windows":
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        rootDir = "C:\\"
    else:  # Unix-like systems
        is_admin = os.geteuid() == 0
        rootDir = "/"
    
    # If not running as admin/root, re-execute script with elevated privileges
    if not is_admin:
        try:
            if platform.system() == "Windows":
                # Create a temp script that will continue processing
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tf:
                    tf.write(open(__file__, 'rb').read())
                    temp_script = tf.name
                
                # Re-run with admin privileges
                subprocess.run(['powershell', 'Start-Process', 'python', 
                               f'"{temp_script}"', f'"{outputFile}"',
                               '-Verb', 'RunAs'], check=True)
            else:
                # For Unix, use sudo to elevate privileges
                writeFileSystemCacheUnix(outputFile)
                return
            return  # Exit original non-elevated process
        except subprocess.SubprocessError:
            print("Warning: Could not obtain elevated privileges. Some files may be inaccessible.")
    
    # Create a memory-efficient scanner that handles errors gracefully
    def scan_with_error_handling(path):
        results = []
        try:
            # Add current directory to results
            results.append(f"{path}\n".encode())
            
            # Process entries in this directory
            with os.scandir(path) as entries:
                for entry in entries:
                    try:
                        if entry.is_symlink():
                            # Skip symlinks to avoid cycles
                            continue
                        
                        if entry.is_file():
                            results.append(f"{entry.path}\n".encode())
                    except (PermissionError, OSError, FileNotFoundError):
                        continue
        except (PermissionError, OSError, FileNotFoundError):
            return results
        
        return results
    
    # Function to process directories recursively
    def process_directory(dir_path):
        all_results = []
        
        # Process the current directory
        results = scan_with_error_handling(dir_path)
        all_results.extend(results)
        
        # Recursively process subdirectories
        try:
            with os.scandir(dir_path) as entries:
                for entry in entries:
                    try:
                        if entry.is_dir() and not entry.is_symlink():
                            subdir_results = process_directory(entry.path)
                            all_results.extend(subdir_results)
                    except (PermissionError, OSError, FileNotFoundError):
                        continue
        except (PermissionError, OSError, FileNotFoundError):
            pass
        
        return all_results
    
    # Get first-level directories for parallel processing
    first_level_dirs = []
    try:
        with os.scandir(rootDir) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    first_level_dirs.append(entry.path)
    except (PermissionError, OSError):
        pass
    
    # Process directories in parallel with large buffer
    with open(outputFile, "wb", buffering=1024*1024) as file:
        # Add root directory
        file.write(f"{rootDir}\n".encode())
        
        # Process first-level directories in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_directory, dir_path): dir_path for dir_path in first_level_dirs}
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    results = future.result()
                    for result in results:
                        file.write(result)
                except Exception as e:
                    print(f"Error processing directory: {e}")
                    continue

def writeFileSystemCacheUnix(outputFile: str) -> None:
    """
    Write a cache of the filesystem structure to the specified output file on Unix-like systems.
    
    Args:
        outputFile: The path where the cache file should be written
    """
    try:
        with open(outputFile, 'w') as f:
            subprocess.run(['sudo', 'find', '/', '-type', 'f', '-o', '-type', 'd'], 
                         stdout=f, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
    except subprocess.SubprocessError:
        print("Warning: Could not access a file")

# If script is executed directly
if __name__ == "__main__":
    from const import FILESYSTEM_CACHE_PATH
    output_file = FILESYSTEM_CACHE_PATH
    writeFileSystemCache(output_file)