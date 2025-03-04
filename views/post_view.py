import sqlite3
import json



def list_posts(url):
    with sqlite3.connect("./database.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            """
        db_cursor.execute(query)

        query_results = db_cursor.fetchall()

        posts=[]
        for row in query_results:
            posts.append(dict(row))
        
        serialized_posts = json.dumps(posts)

    return serialized_posts

def retrieve_post(pk):
    with sqlite3.connect("./databse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            WHERE p.id = ?
            """, (pk,))

        query_results = db_cursor.fetchone()

        serialized_post = json.dumps(dict(query_results))

        return serialized_post


