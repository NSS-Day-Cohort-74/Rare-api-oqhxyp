import sqlite3
import json

def list_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT
                c.id,
                c.label
            FROM Categories c
            ORDER BY c.label ASC
            """
        db_cursor.execute(query)

        query_results = db_cursor.fetchall()

        categories=[]
        for row in query_results:
            categories.append(dict(row))
        
        serialized_categories = json.dumps(categories)

    return serialized_categories


def create_category(category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Categories
            (label)
        VALUES
            (?)
        """,
            (category_data["label"],),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def update_category(id, category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Categories
                SET
                    label = ?
            WHERE id = ?
            """,
            (category_data['label'], id)
        )
    return True if db_cursor.rowcount > 0 else False



def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Categories WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
