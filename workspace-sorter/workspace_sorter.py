import shutil
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server with a clear description
mcp = FastMCP("Workspace Sorter")

@mcp.tool()
def list_files(directory_path: str) -> list[str]:
    """
    Lists all files in the specified directory path (non-recursively).
    It ignores hidden files (like .DS_Store) and environment/config files 
    (like workspace_sorter.py, pyproject.toml, uv.lock, and .venv) to keep the list clean.
    
    Args:
        directory_path (str): The absolute path of the directory to list files from.
        
    Returns:
        list[str]: A list of filenames found, or an error message if the path is invalid.
    """
    path = Path(directory_path).resolve()
    if not path.exists() or not path.is_dir():
        return [f"Error: {directory_path} is not a valid directory."]
    
    # List of files/folders to ignore during sorting
    ignore_list = {
        ".DS_Store", 
        "workspace_sorter.py", 
        "pyproject.toml", 
        "uv.lock", 
        ".venv"
    }
    
    try:
        return [
            item.name 
            for item in path.iterdir() 
            if item.is_file() 
            and not item.name.startswith('.') 
            and item.name not in ignore_list
        ]
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

@mcp.tool()
def create_directory(directory_path: str) -> str:
    """
    Creates a new directory (and any necessary parent directories) at the specified path.
    
    Args:
        directory_path (str): The absolute path of the directory to be created.
        
    Returns:
        str: A success or error message.
    """
    path = Path(directory_path).resolve()
    try:
        path.mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@mcp.tool()
def move_file(source_path: str, destination_path: str) -> str:
    """
    Moves a file from the source path to the destination path.
    If the destination directory does not exist yet, it will be automatically created.
    
    Args:
        source_path (str): The absolute path of the file to move.
        destination_path (str): The absolute path of the destination (including filename).
        
    Returns:
        str: A success or error message.
    """
    src = Path(source_path).resolve()
    dest = Path(destination_path).resolve()
    try:
        if not src.exists():
            return f"Error: Source file {source_path} does not exist."
        if src.is_dir():
            return f"Error: {source_path} is a directory. This tool only moves files."
            
        # Automatically ensure the parent directory of the destination exists before moving
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Perform the move
        shutil.move(str(src), str(dest))
        return f"Successfully moved {src.name} to {dest}"
    except Exception as e:
        return f"Error moving file: {str(e)}"

if __name__ == "__main__":
    # Start the stdio transport bridge expected by mcporter / OpenClaw
    mcp.run(transport="stdio")
