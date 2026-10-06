import sqlite3

DATABASE_PATH = "calculator.db"

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open("src/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def add_history(expression: str, result: float):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calculation_history (expression, result) VALUES (?, ?)",
        (expression, result)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, expression, result, created_at FROM calculation_history ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "expression": row["expression"],
            "result": row["result"],
            "time": row["created_at"]
        }
        for row in rows
    ]

def delete_history_by_id(record_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculation_history WHERE id = ?", (record_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def clear_all_history() -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculation_history")
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected
