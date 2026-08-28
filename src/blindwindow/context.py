# src/blindwindow/context.py
from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

APP_NAME = "blindwindow"
APP_NAME_PRETTY = "Blindwindow"
IMPORT_NAME = "blindwindow"
SRC_FOLDER_NAME = "blindwindow"
DESCRIPTION_STR = "A Python application."
APP_DIR = Path.home() / ".blindwindow"
LOG_FILE_PATH = APP_DIR / "blindwindow.log"
SERVICE = APP_NAME
CONFIG_PATH = APP_DIR / "config.json"
SECRET_PATH = APP_DIR / "vault.db"
ENV_PATH = PROJECT_ROOT / ".env"
