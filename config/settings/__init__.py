import os
import json
from pathlib import Path

# Load environment from version.json
base_dir = Path(__file__).resolve().parent.parent.parent
version_path = base_dir / "version.json"

try:
    with open(version_path) as f:
        version_data = json.load(f)
        env = version_data.get("environment", "local")
except Exception as e:
    raise RuntimeError(f"Unable to load environment from version.json - {e}")

# Route to the correct settings module
if env == "local":
    from .local import *
elif env == "staging":
    from .staging import *
elif env == "production":
    from .production import *
else:
    raise ImportError(f"Unknown environment in version.json: {env}")