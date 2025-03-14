# Rare Server
The Rare Server is the backend for the Rare Client application. The Rare application allows logged-in users to:

-View posts created by others that have been approved by admins
-View user profiles
-Create, edit, and delete their own posts
-Create and manage comments

The API supports CRUD (Create, Read, Update, Delete) operations through the use of GET, POST, PUT, and DELETE HTTP methods.

## Base Url
`http://localhost:8088`

## Authentication
The API requires authentication for most endpoints. Ensure users are logged in to access protected resources.

## Getting Started:
1. Clone the github repository SSH
2. Run `pipenv shell` to start the virtual environment
3. Run `pipenv install` to install the dependencies
4. Create a `db.sqlite3` file
5. Run the commands in the `loaddata.sql` file to create the tables in the database


## Endpoints
### Users

* Get All Users * 
GET /users
Returns a list of all registered users.

* Get a Single User *
GET /users/{id}
Returns details of a specific user by ID.

*Update a User*
PUT /deactivateUser/{id}
Sets user to deactivated.

PUT /reactivateUser/{id}
Sets user to active.

*Create New User and Login*
POST /register
Creates a new user and returns their token.

GET /login
Verifies that a user is in the database and that their login information is correct. 

### Categories

* Get All Categories*
GET /categories
Returns a list of all categories.

* Create Categories*
POST /categories
Adds a new categories to the list of categories

* Delete Category*
DELETE /categories/{id}
Removes a category from the database

### Tags
* Get All tag*
GET /tag
Returns a list of all tag.

* Create tag*
POST /tag
Adds a new tag to the list of tags

* Delete Category*
DELETE /postTag/{post.id}
Removes all tags with a specific postId from the database

## Status Codes
- 200 OK – Request was successful
- 201 Created – Resource was successfully created
- 400 Bad Request – Invalid request syntax or parameters
- 404 Not Found – Requested resource not found
- 500 Internal Server Error – An error occurred on the server




