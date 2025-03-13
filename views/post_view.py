import sqlite3
import json


def list_posts(url):
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
                p.approved,
                c.id as category_id,
                c.label as category_label,
                u.id as user_id,
                u.first_name,
                u.last_name,
                u.email,
                u.username,
                u.bio,
                t.id as tag_id,
                t.label as tag_label
            FROM Posts p
            LEFT JOIN Categories c ON c.id = p.category_id
            LEFT JOIN Users u ON u.id = p.user_id
            LEFT JOIN PostTags pt ON pt.post_id = p.id
            LEFT JOIN Tags t ON t.id = pt.tag_id
            ORDER BY p.publication_date DESC
            """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()

        posts_dict = {}

        for row in query_results:
            post_id = row["id"]
            if post_id not in posts_dict:
                posts_dict[post_id] = {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "category_id": row["category_id"],
                    "title": row["title"],
                    "publication_date": row["publication_date"],
                    "image_url": row["image_url"],
                    "content": row["content"],
                    "approved": row["approved"],
                    "categories": {
                        "id": row["category_id"],
                        "label": row["category_label"]
                    } if row["category_id"] else None,
                    "user": {
                        "id": row["user_id"],
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "email": row["email"],
                        "username": row["username"],
                        "bio": row["bio"]
                    } if row["user_id"] else None,
                    "tags": []
                }

            if row["tag_id"]:
                posts_dict[post_id]["tags"].append({
                    "id": row["tag_id"],
                    "label": row["tag_label"]
                })

        posts = list(posts_dict.values())
        serialized_posts = json.dumps(posts)

    return serialized_posts


def retrieve_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                u.id userId,
                u.first_name,
                u.last_name,
                c.id categoryId,
                c.label
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (pk,),
        )

        query_results = db_cursor.fetchone()

        post = {
            "id": query_results["id"],
            "user_id": query_results["user_id"],
            "user": {
                "id": query_results["userId"],
                "first_name": query_results["first_name"],
                "last_name": query_results["last_name"],
            },
            "category_id": query_results["category_id"],
            "categories": {
                "id": query_results["categoryId"],
                "label": query_results["label"],
            },
            "title": query_results["title"],
            "publication_date": query_results["publication_date"],
            "image_url": query_results["image_url"],
            "content": query_results["content"],
            "approved": query_results["approved"],
        }

        serialized_post = json.dumps(post)

        return serialized_post


def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
            ),
        )

        # Return the row data that was created above with the new post
        new_post_created_id = int(db_cursor.lastrowid)
        conn.commit

        # Write the SQL Query that will be returned
        db_cursor.execute(
            """
            SELECT 
                p.id
            FROM Posts p
            WHERE p.id = ?
        """,
            (new_post_created_id,),
        )
        query_results = db_cursor.fetchone()

        new_post = dict(query_results)

        return new_post

        return {"message": "create post was a success!"}


def update_post(id, post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Posts
                SET
                    user_id = ?,
                    category_id = ?,
                    title = ?,
                    publication_date = ?,
                    image_url = ?, 
                    content = ?,
                    approved = ?
            WHERE id = ?
            """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
                id,
            ),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Posts WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount
        
    return True if number_of_rows_deleted > 0 else False

