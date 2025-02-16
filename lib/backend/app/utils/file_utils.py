import os

def ensure_directory_exists(directory):
    """Ensure that the specified directory exists and is writable."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.access(directory, os.W_OK):
        raise PermissionError(f"Cannot write to directory: {directory}")