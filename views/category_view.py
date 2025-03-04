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
            """
        db_cursor.execute(query)

        query_results = db_cursor.fetchall()

        categories=[]
        for row in query_results:
            categories.append(dict(row))
        
        serialized_categories = json.dumps(categories)

    return serialized_categories


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


# def update_dock(id, dock_data):
#     with sqlite3.connect("./shipping.db") as conn:
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#             UPDATE Dock
#                 SET
#                     location = ?,
#                     capacity = ?
#             WHERE id = ?
#             """,
#             (dock_data['location'], dock_data['capacity'], id)
#         )

#     return True if db_cursor.rowcount > 0 else False



def delete_category():
    pass
