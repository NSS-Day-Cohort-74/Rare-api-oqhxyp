import sqlite3
import json



def list_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
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
    with sqlite3.connect("./db.sqlite3") as conn:
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

def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (post_data["user_id"],post_data["category_id"],post_data["title"],post_data["publication_date"],post_data["image_url"],post_data["content"],post_data["approved"]),)
        return {"message": "create post was a success!"}