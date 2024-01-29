import sqlite3

def delete_data(n):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM passwords WHERE rowid = {n+1};")
    cursor.execute(f"UPDATE passwords SET rowid=rowid-1 WHERE rowid>{n+1};")

    conn.commit()
    conn.close()