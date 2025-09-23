import oracledb
from pathlib import Path
from config.config import setup
import os

def connect():
    username, password, dsn, wallet_dir = setup()
    os.environ["TNS_ADMIN"] = wallet_dir
    sqlnet = Path(wallet_dir) / "sqlnet.ora"
    if sqlnet.exists():
        txt = sqlnet.read_text(errors="ignore")
        for ln in txt.splitlines():
            if "WALLET" in ln.upper():
                print("sqlnet.ora:", ln, flush=True)
            else:
                print(f"`{sqlnet}` not found", flush=True)
        try:
            oracledb.init_oracle_client(config_dir=wallet_dir)
            print("init_oracle_client OK", flush=True)
            conn = oracledb.connect(user=username, password=password, dsn=dsn)
            print("connection is OK", flush=True)
            return conn
        except Exception as e:
            print("init_oracle_client exception (continuing):", type(e).__name__, e)