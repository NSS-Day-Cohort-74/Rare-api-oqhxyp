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
                """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = dict(row)
            
          
            if expand_categories:
                categories = {
                    "id": post.pop("c_id"), 
                    "label": post.pop("label")
                }
                post["categories"] = categories
            
            
            if expand_users:
                user = {
                    "id": post.pop("u_id"),
                    "first_name": post.pop("first_name"),
                    "last_name": post.pop("last_name"),
                    "email": post.pop("email"),
                    "username": post.pop("username"),
                    "bio": post.pop("bio")
                }
                post["user"] = user
            
            posts.append(post)
            
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