import sqlite3
import json
from datetime import datetime

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active, is_admin) values (?, ?, ?, ?, ?, ?, ?, 1, 0)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })

def list_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    
        query = """
            SELECT 
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.profile_image_url,
                u.created_on,
                u.active,
                u.is_admin
            FROM Users u
            ORDER by u.username
        """
        db_cursor.execute(query)

        query_results = db_cursor.fetchall()

        users=[]
        for row in query_results:
            users.append(dict(row))
        
        serialized_users = json.dumps(users)

    return serialized_users

def retrieve_user(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.profile_image_url,
                u.created_on,
                u.active,
                u.is_admin
            FROM Users u
            WHERE u.id = ?
            """, (pk,))

        query_results = db_cursor.fetchone()

        serialized_user = json.dumps(dict(query_results))

    return serialized_user

def update_user(pk, data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE USERS
                    SET
                        id = ?,
                        is_admin = ?
                WHERE id = ?
            """, (
                data["id"],
                data["is_admin"],
                data["id"],
            )
        )

        rows_affected = db_cursor.rowcount
    
    return True if rows_affected > 0 else False 

def reactivate_user(data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE USERS
                    SET
                        id = ?,
                        active = ?
                WHERE id = ?
            """, (
                data["id"],
                data["active"],
                data["id"],
            )
        )

        rows_affected = db_cursor.rowcount
    
    return True if rows_affected > 0 else False 

def deactivate_user(data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE USERS
                    SET
                        id = ?,
                        active = ?
                WHERE id = ?
            """, (
                data["id"],
                data["active"],
                data["id"],
            )
        )

        rows_affected = db_cursor.rowcount
    
    return True if rows_affected > 0 else False 
