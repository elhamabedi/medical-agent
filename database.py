import sqlite3
from pathlib import Path
from typing import Optional


DB_PATH = Path("data/medical_agent.db")


def init_database() -> None:
    
    DB_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT,
            weight REAL,
            height REAL,
            blood_type TEXT,
            medical_history TEXT,
            allergies TEXT,
            medications TEXT,
            lifestyle TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            assistant_response TEXT NOT NULL,
            is_emergency INTEGER DEFAULT 0,
            urgency_level TEXT DEFAULT 'non-emergency',
            created_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            symptom TEXT NOT NULL,
            severity INTEGER,
            duration TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f" Database initialized at: {DB_PATH}")


def get_db_connection() -> sqlite3.Connection:
  
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn


def check_database_exists() -> bool:
   
    return DB_PATH.exists()

init_database()