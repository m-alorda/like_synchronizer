from pathlib import Path
import logging
import logging.config

import yaml

PROJECT_DIR = Path(__file__).resolve().parent.parent

_CONFIG_FILE = PROJECT_DIR / "config/config.yaml"
with _CONFIG_FILE.open(encoding="utf-8") as f:
    config = yaml.safe_load(f)

YOUTUBE_SECRET_FILE_PATH = (
    PROJECT_DIR / config["secrets"]["path"] / "youtube_client_secret.json"
)

_LOGGING_CONFIG_FILE = PROJECT_DIR / config["log"]["configFile"]
with _LOGGING_CONFIG_FILE.open() as f:
    _logging_config = yaml.safe_load(f)
logging.config.dictConfig(_logging_config)

log = logging.getLogger()
log.debug("Loaded logging config")

_SECRET_CONFIG_FILE = PROJECT_DIR / config["secrets"]["path"] / "config.yaml"
with _SECRET_CONFIG_FILE.open(encoding="utf-8") as f:
    secret_config = yaml.safe_load(f)

log.debug("Loaded config")
