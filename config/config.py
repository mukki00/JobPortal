import os


def setup():
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")
    wallet_dir = os.getenv("DB_WALLET_DIR")
    return username, password, dsn, wallet_dir