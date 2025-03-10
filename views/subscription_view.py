import sqlite3
import json

def list_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #SQL Query to Return Subscriptions Table
        db_cursor.execute("""
            SELECT
                s.id,
                s.follower_id,
                s.author_id,
                s.created_on
            FROM Subscriptions s    
        """)
        query_results = db_cursor.fetchall()

        subscriptions = []

        for row in query_results:
            subscriber = {
                "id": row['id'],
                "follower_id": row['follower_id'],
                "author_id": row['author_id'],
                "created_on": row['created_on']
            }
            subscriptions.append(subscriber)

        serialized_subscriptions= json.dumps(subscriptions)

        return serialized_subscriptions
    
def create_subscription(data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            INSERT INTO Subscriptions (follower_id, author_id, created_on)
                VALUES(?, ?, ?)
        """,
        (data["follower_id"], data["author_id"], data["created_on"]),)

        new_subscription_created_id = int(db_cursor.lastrowid)
        conn.commit

        db_cursor.execute("""
            SELECT
                s.id
            FROM Subscriptions s
            WHERE id = ?
        """,(new_subscription_created_id,))
        query_results = db_cursor.fetchone()

        new_subscription = dict(query_results)
        return new_subscription

def delete_subscription(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM Subscriptions WHERE id = ? 
        """,(pk,))

        number_of_rows_deleted = db_cursor.rowcount

        return True if number_of_rows_deleted > 0 else False
    