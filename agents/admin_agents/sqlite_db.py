import sqlite3

DB_NAME = "data/candidates.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            experiences TEXT,
            tech_stack TEXT,
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_sqlite(candidates):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for candidate in candidates:
        c.execute("INSERT INTO candidates (name, email, experiences, tech_stack, skills) VALUES (?, ?, ?, ?, ?)", 
                  (candidate.get("name"), candidate.get("email"), candidate.get("experiences"), candidate.get("tech_stack"), candidate.get("skills")))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, email, experiences, tech_stack, skills FROM candidates")
    results = c.fetchall()
    conn.close()
    return results


