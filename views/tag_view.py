import sqlite3
import json

def list_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT 
                t.id,
                t.label
            FROM Tags t
        """
        db_cursor.execute(query)

        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    
    return serialized_tags

def create_tag(tag_data):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
        """ 
        INSERT INTO Tags (label) 
        VALUES (?)
        """, (tag_data["label"],),
        ) 
        return {"message": "tag has been posted" }

def create_posttag(posttag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags (post_id, tag_id)
            VALUES (?, ?)
        """,
        (posttag_data["post_id"],posttag_data["tag_id"]),)
        return {"message": "created post tags successfully!"}

def delete_tag():
    pass