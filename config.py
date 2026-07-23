from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "doc"
PREMISES_FILE = DATA_DIR / "premises.csv"
TRADE_PLACES_FILE = DATA_DIR / "trade_places.csv"
SPECIAL_OFFERS_FILE = DATA_DIR / "special_offers.csv"
APPLICATIONS_FILE = DATA_DIR / "applications.csv"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Add it to .env or environment variables.")
