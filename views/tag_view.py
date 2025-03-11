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


def list_PostTags(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT 
                pt.id,
                pt.post_id,
                pt.tag_id
            FROM PostTags pt
        """

        expand_tags = False
        if "query_params" in url and "_expand" in url["query_params"] and "tag" in url["query_params"]["_expand"]:
            expand_tags = True
            query = """
                SELECT
                    pt.id,
                    pt.post_id,
                    pt.tag_id,
                    t.id as tagId,
                    t.label
                FROM PostTags pt
                JOIN Tags t ON t.id = pt.tag_id
                """
        db_cursor.execute(query)
        query_results = db_cursor.fetchall()
          
        postTags = []

        for row in query_results:
            row_dict = dict(row)  
            
            post_tag = {
                "id": row_dict["id"],
                "post_id": row_dict["post_id"],
                "tag_id": row_dict["tag_id"]
            }
            
            
            if expand_tags:
                post_tag["tag"] = {
                    "id": row_dict["tagId"],
                    "label": row_dict["label"]
                }
                
            postTags.append(post_tag)

        serialized_postTags = json.dumps(postTags)
    
    return serialized_postTags

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


def get_post_tags(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT 
                t.id,
                t.label
            FROM Tags t
            JOIN PostTags pt ON pt.tag_id = t.id
            WHERE pt.post_id = ?
        """
        
        db_cursor.execute(query, (post_id,))
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    
    return serialized_tags


def delete_post_tags(post_id):
    """
    Deletes all tag associations for a specific post
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Query to delete all tag associations for a specific post
        query = """
            DELETE FROM PostTags
            WHERE post_id = ?
        """
        
        db_cursor.execute(query, (post_id,))
        
        # Check if any rows were affected
        rows_deleted = db_cursor.rowcount
        
    return {"message": f"Deleted {rows_deleted} tag associations for post {post_id}"}


def update_post_tags(post_id, tag_data):
    """
    Updates the tags associated with a specific post.
    First removes all existing tag associations, then adds the new ones.
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        # First delete existing associations
        delete_query = """
            DELETE FROM PostTags
            WHERE post_id = ?
        """
        db_cursor.execute(delete_query, (post_id,))
        deleted_count = db_cursor.rowcount
        
        # Then add new associations
        rows_affected = 0
        for tag_id in tag_data["tag_ids"]:
            insert_query = """
                INSERT INTO PostTags (post_id, tag_id)
                VALUES (?, ?)
            """
            db_cursor.execute(insert_query, (post_id, tag_id))
            rows_affected += db_cursor.rowcount
            
        return {
            "message": f"Updated tags for post {post_id}. Removed {deleted_count} previous associations and added {rows_affected} new tag associations."
        }