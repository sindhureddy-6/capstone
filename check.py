import sqlite3
import json

db = sqlite3.connect("sessions.db")
cur = db.cursor()

print("Tables in your DB:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cur:
    print("  →", row[0])

print("\nYour saved memory:")
cur.execute("SELECT user_id, state FROM sessions")
for row in cur:
    state = json.loads(row[1]) if row[1] else {}
    print(f"\nUser: {row[0]}")
    print(f"Name      : {state.get('user_name', 'Not saved yet')}")
    print(f"Moods     : {state.get('past_moods', [])}")
    print(f"Messages  : {state.get('message_count', 0)}")
    print(f"Favorite  : {state.get('favorite_coping', 'Not set')}")
    print("-" * 50)

db.close()
print("\nDone! If you see your name and moods → memory is working perfectly!")