"""Configuration file for Kindle reading data sync"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)

# Amazon Kindle URL (amazon.cn service has been discontinued)
KINDLE_HISTORY_URL = "https://www.amazon.com/kindle/reading/insights/data"

# Headers for requests
KINDLE_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Data file paths
KINDLE_DATA_FILE = DATA_DIR / "kindle_data.json"
READING_DATA_FILE = DATA_DIR / "reading_data.json"
