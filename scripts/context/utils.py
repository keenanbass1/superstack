import os
import logging
from pathlib import Path
import yaml
import json
import shutil
import re
from typing import Dict, List, Optional, Any, Union

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Name for the logger
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to the logger
        logger.addHandler(handler)
    
    return logger

def load_yaml_config(config_path):
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        dict: Configuration data
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the config file has invalid YAML syntax
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML configuration: {str(e)}")

def ensure_dir(directory: str) -> str:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path
        
    Returns:
        str: The directory path
    """
    if directory:
        os.makedirs(directory, exist_ok=True)
    return directory

def backup_file(file_path, backup_dir=None):
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backups (defaults to same directory with .bak extension)
        
    Returns:
        str: Path to the backup file
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if backup_dir:
        backup_path = Path(backup_dir) / f"{file_path.name}.bak"
        ensure_dir(backup_dir)
    else:
        backup_path = file_path.with_suffix(f"{file_path.suffix}.bak")
    
    shutil.copy2(file_path, backup_path)
    return str(backup_path)

def extract_module_name(file_path: str) -> str:
    """
    Extract module name from file path.
    
    Args:
        file_path: Path to the module file
        
    Returns:
        str: Module name without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def write_json(file_path: str, data: Union[Dict, List]) -> None:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Data to write
    """
    ensure_dir(os.path.dirname(file_path))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def read_json(file_path: str) -> Dict:
    """
    Read JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger = setup_logger('context_utils')
        logger.error(f"Error reading JSON file {file_path}: {str(e)}")
        return {}

def read_file_content(file_path: str) -> str:
    """
    Read content from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: File content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file_content(file_path: str, content: str) -> None:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
    """
    # Ensure directory exists
    ensure_dir(os.path.dirname(file_path))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_context_blocks(content: str) -> List[str]:
    """
    Extract context blocks from content.
    
    Args:
        content: Module content
        
    Returns:
        list: Extracted context blocks
    """
    # Match content between <context> and </context> tags
    pattern = r'<context>(.*?)</context>'
    blocks = re.findall(pattern, content, re.DOTALL)
    
    # Clean up whitespace
    return [block.strip() for block in blocks]

def generate_diff(original: str, optimized: str, file_name: str = "module") -> str:
    """
    Generate a simple diff between original and optimized content.
    
    Args:
        original: Original content
        optimized: Optimized content
        file_name: Name for the diff file
        
    Returns:
        str: Diff content in a readable format
    """
    import difflib
    
    original_lines = original.splitlines()
    optimized_lines = optimized.splitlines()
    
    diff = difflib.unified_diff(
        original_lines,
        optimized_lines,
        fromfile=f"{file_name}.original",
        tofile=f"{file_name}.optimized",
        lineterm=""
    )
    
    return "\n".join(diff)

def safe_filename(name: str) -> str:
    """
    Convert a string to a safe filename.
    
    Args:
        name: Input string
        
    Returns:
        str: Safe filename
    """
    # Replace unsafe characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', name) 