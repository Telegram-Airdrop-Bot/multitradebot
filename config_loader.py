import yaml
import threading
import os

# Look for config.yaml in current directory (parent of gui/)
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
_config_cache = None
_config_lock = threading.Lock()

def get_config():
    global _config_cache
    with _config_lock:
        try:
            with open(_CONFIG_PATH, 'r') as f:
                _config_cache = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f'Failed to load config: {e}')
        return _config_cache

# Optionally, add a reload_config() if you want to force reload

def reload_config():
    global _config_cache
    with _config_lock:
        _config_cache = None
    return get_config() 