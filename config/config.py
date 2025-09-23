import os
from pathlib import Path

def setup():
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")
    root_dir = Path(__file__).resolve().parent.parent
    wallet_dir = str(root_dir / "Resources/Wallet_FREEPDB1")
    return username, password, dsn, wallet_dir