from core.knowledge.quran_db import QuranDatabase
from core.knowledge.sacred_scanner import SacredScanner
import logging
import sqlite3
import os

logging.basicConfig(level=logging.INFO)

def full_clean_reset():
    # 1. Purge existing database
    db_path = "core/knowledge/data/quran.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 2. Rebuild from scratch
    quran_db = QuranDatabase()
    scanner = SacredScanner()
    
    # 3. Forcefully rebuild all structures
    if not scanner._initialize():
        raise RuntimeError("Atomic initialization failed")
    
    # 4. Verify
    required_themes = ['creation', 'mercy', 'prophets']
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for theme in required_themes:
            cursor.execute("SELECT COUNT(*) FROM themes WHERE theme=?", (theme,))
            if cursor.fetchone()[0] < 1:
                raise ValueError(f"Theme {theme} missing")
    
    logging.info("SUCCESS: Database rebuilt with thematic index")

if __name__ == "__main__":
    full_clean_reset()