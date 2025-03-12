import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# View Imports 

from views import list_posts, retrieve_post, create_post, update_post, delete_post
from views import list_tags, create_tag, create_posttag, get_post_tags, delete_post_tags, update_post_tags, list_PostTags
from views import list_categories, update_category, delete_category, create_category
from views import create_user, login_user, retrieve_user, list_users 
from views import list_subscriptions, create_subscription, delete_subscription, subscriptions_posts
from views import create_comment, list_comments, delete_comment


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Rare"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        path_parts = self.path.split('/')
        if len(path_parts) >= 4 and path_parts[1] == "tags" and path_parts[2] == "posts" and path_parts[3].isdigit():
            post_id = int(path_parts[3])
            response_body = get_post_tags(post_id)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)


        if url["requested_resource"] == "posttags":
            response_body = list_PostTags(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
        
        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = retrieve_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_posts(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            response_body = list_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # elif url["requested_resource"] == "tags" and url["query_params"] and "post_id" in url["query_params"]:
        #     post_id = url["query_params"]["post_id"][0]
        #     response_body = get_post_tags(post_id)
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            response_body = list_categories(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        elif url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            response_body = list_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        elif url["requested_resource"] == "comments":
            response_body = list_comments(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "subscriptions":
            response_body = list_subscriptions()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        elif url["requested_resource"] == "favoriteSubscriptions":
            response_body = subscriptions_posts(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        


    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        data = json.loads(request_body)

        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            response_body = create_user(data)
            if response_body:                                   
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
      

        elif url["requested_resource"]== "login":
            response_body = login_user(data)
            if response_body:
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        elif url["requested_resource"] == "posts":
            response_body = create_post(data)
            if response_body:                                   
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        elif url["requested_resource"] == "categories":
            response_body = create_category(data)
            if response_body:                                   
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        
        elif url["requested_resource"] == "posttags":
            response_body = create_posttag(data)
            if response_body:                                 
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        elif url["requested_resource"] == "tags":
            response_body = create_tag(data)
            if response_body: 
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        elif url["requested_resource"]=="subscriptions":
            response_body = create_subscription(data)
            if response_body:
                return self. response(json.dumps(response_body),status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "comments":
            response_body = create_comment(data)
            if response_body: 
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        else:
            return self.response("Resource not found", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        # Special case for tags/posts/{id} route
        path_parts = self.path.split('/')
        if len(path_parts) >= 4 and path_parts[1] == "tags" and path_parts[2] == "posts" and path_parts[3].isdigit():
            post_id = int(path_parts[3])
            response_body = delete_post_tags(post_id)
            return self.response(json.dumps(response_body), status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        elif url["requested_resource"] == "subscriptions":
            if pk != 0:
                successfully_deleted = delete_subscription(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
            
        elif url["requested_resource"]=="posts":
            if pk !=0:
                successfully_deleted=delete_post(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        elif url["requested_resource"]=="comments":
            if pk !=0:
                successfully_deleted=delete_comment(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
              
        else:
            return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def do_PUT(self):
        """Handle PUT requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

    
        path_parts = self.path.split('/')
        if len(path_parts) >= 4 and path_parts[1] == "tags" and path_parts[2] == "posts" and path_parts[3].isdigit():
            post_id = int(path_parts[3])
            response_body = update_post_tags(post_id, request_body)
            return self.response(json.dumps(response_body), status.HTTP_200_SUCCESS.value)

        # Handle other PUT routes
        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        
        elif url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = update_post(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)



# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES BUT IMPORTANT FOR SETTING THE RIGHT PORT TO LISTEN TO
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()
    print("SERVER IS RUNNING... MAYBE???")