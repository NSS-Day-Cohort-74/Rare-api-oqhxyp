import sqlite3
import json


def create_comment(comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Comments (post_id, author_id, content)
        VALUES (?, ?, ?)
        """,
            (
                comment_data["post_id"],
                comment_data["author_id"],
                comment_data["content"],
            ),
        )

    return True if db_cursor.rowcount > 0 else False


def list_comments(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        query = """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content
            FROM Comments c
            """

        expand_post = False
        expand_author = False

        if url and "query_params" in url and "_expand" in url["query_params"]:
            if "post" in url["query_params"]["_expand"]:
                expand_post = True
            if "author" in url["query_params"]["_expand"]:
                expand_author = True

        if expand_post and expand_author:
            query = """
                SELECT
                    c.id,
                    c.post_id,
                    c.author_id,
                    c.content,
                    p.title,
                    u.username
                    
                FROM Comments c
                JOIN Posts p ON c.post_id = p.id
                JOIN Users u On c.author_id = u.id
                """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()

        comments = []
        for row in query_results:
            comment = dict(row)

            if expand_post:
                post = {"title": comment.pop("title")}
                comment["post"] = post

            if expand_author:
                author = {"username": comment.pop("username")}
                comment["author"] = author

            comments.append(comment)

        serialized_comments = json.dumps(comments)

    return serialized_comments


def delete_comment(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """DELETE From Comments WHERE id=?
    """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
