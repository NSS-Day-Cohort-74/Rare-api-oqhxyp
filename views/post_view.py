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
                p.approved
            FROM Posts p
            ORDER BY p.publication_date DESC
            """

        expand_categories = False
        expand_users = False

        if url and "query_params" in url and "_expand" in url["query_params"]:
            if "categories" in url["query_params"]["_expand"]:
                expand_categories = True
            if "users" in url["query_params"]["_expand"]:
                expand_users = True

        if expand_categories and expand_users:
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
                    c.id as c_id,
                    c.label,
                    u.id as u_id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.username,
                    u.bio
                FROM Posts p
                JOIN Categories c ON c.id = p.category_id
                JOIN Users u ON u.id = p.user_id
                ORDER BY p.publication_date DESC
                """
        elif expand_categories:
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
                    c.id as c_id,
                    c.label
                FROM Posts p
                JOIN Categories c ON c.id = p.category_id
                ORDER BY p.publication_date DESC
                """
        elif expand_users:
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
                    u.id as u_id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.username,
                    u.bio
                FROM Posts p
                JOIN Users u ON u.id = p.user_id
                ORDER BY p.publication_date DESC
                """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = dict(row)

            if expand_categories:
                categories = {"id": post.pop("c_id"), "label": post.pop("label")}
                post["categories"] = categories

            if expand_users:
                user = {
                    "id": post.pop("u_id"),
                    "first_name": post.pop("first_name"),
                    "last_name": post.pop("last_name"),
                    "email": post.pop("email"),
                    "username": post.pop("username"),
                    "bio": post.pop("bio"),
                }
                post["user"] = user

            posts.append(post)

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

