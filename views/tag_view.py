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
        expand_posts = False
        expand_users = False
        expand_categories = False

        if "query_params" in url and "_expand" in url["query_params"]:
            if "tag" in url["query_params"]["_expand"]:
                expand_tags = True
            if "post" in url["query_params"]["_expand"]:
                expand_posts = True
            if "user" in url["query_params"]["_expand"]:
                expand_users = True
            if "category" in url["query_params"]["_expand"]:
                expand_categories = True

        if expand_tags or expand_posts or expand_users or expand_categories:
            query = """
                SELECT
                    pt.id,
                    pt.post_id,
                    pt.tag_id,
                    t.id as tagId,
                    t.label,
                    p.id as postId,
                    p.user_id,
                    p.category_id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved,
                    u.id as userId,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.username,
                    u.bio,
                    c.id as categoryId,
                    c.label as categoryLabel
                FROM PostTags pt
                LEFT JOIN Tags t ON t.id = pt.tag_id
                LEFT JOIN Posts p ON p.id = pt.post_id
                LEFT JOIN Users u ON p.user_id = u.id
                LEFT JOIN Categories c ON p.category_id = c.id
            """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()

        postTags = []

        for row in query_results:
            row_dict = dict(row)

            post_tag = {
                "id": row_dict["id"],
                "post_id": row_dict["post_id"],
                "tag_id": row_dict["tag_id"],
            }

            if expand_tags:
                post_tag["tag"] = {"id": row_dict["tagId"], "label": row_dict["label"]}
            if expand_posts:
                post_tag["post"] = {
                    "id": row_dict["postId"],
                    "user_id": row_dict["user_id"],
                    "category_id": row_dict["category_id"],
                    "title": row_dict["title"],
                    "publication_date": row_dict["publication_date"],
                    "image_url": row_dict["image_url"],
                    "content": row_dict["content"],
                    "approved": row_dict["approved"],
                }
            if expand_users:
                post_tag["post"]["user"] = {
                    "id": row_dict["userId"],
                    "first_name": row_dict["first_name"],
                    "last_name": row_dict["last_name"],
                    "email": row_dict["email"],
                    "username": row_dict["username"],
                    "bio": row_dict["bio"],
                }
            if expand_categories:
                post_tag["post"]["categories"] = {
                    "id": row_dict["categoryId"],
                    "label": row_dict["categoryLabel"],
                }

            postTags.append(post_tag)

        serialized_postTags = json.dumps(postTags)

    return serialized_postTags

def create_tag(tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """ 
        INSERT INTO Tags (label) 
        VALUES (?)
        """,
            (tag_data["label"],),
        )
        return {"message": "tag has been posted"}


def create_posttag(posttag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO PostTags (post_id, tag_id)
            VALUES (?, ?)
        """,
            (posttag_data["post_id"], posttag_data["tag_id"]),
        )
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
